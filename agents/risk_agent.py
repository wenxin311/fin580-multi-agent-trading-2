import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from schemas.signal_schema import SignalOutput
from schemas.risk_schema import RiskOutput

class RiskManagerAgent:
    def __init__(self, max_vix=30.0, min_conviction=3, max_drawdown=0.20):
        self.max_vix = max_vix
        self.min_conviction = min_conviction
        self.max_drawdown = max_drawdown
        self._cache = {}
        
    def get_market_data(self, ticker: str, date_str: str, window_days: int = 7) -> pd.DataFrame:
        cache_key = f"{ticker}_{date_str}_{window_days}"
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            start_date = target_date - timedelta(days=window_days)
            end_date = target_date + timedelta(days=1)
            
            data = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"), progress=False)
            if not data.empty and isinstance(data.columns, pd.MultiIndex):
                data = data.xs(ticker, level=1, axis=1) # Flatten multiindex for specific ticker
                
            self._cache[cache_key] = data
            return data
        except Exception as e:
            print(f"   [WARNING] Error fetching {ticker} for {date_str}: {e}")
            return pd.DataFrame()

    def get_vix_for_date(self, date_str: str) -> float:
        data = self.get_market_data("^VIX", date_str, window_days=7)
        if data.empty:
            return 20.0
        return float(data['Close'].iloc[-1])
        
    def get_asset_drawdown(self, date_str: str) -> float:
        # Fetch last 30 days of Brent Crude (BZ=F) to calculate drawdown
        data = self.get_market_data("BZ=F", date_str, window_days=30)
        if data.empty or len(data) < 2:
            return 0.0
            
        close_prices = data['Close']
        current_price = float(close_prices.iloc[-1])
        max_price = float(close_prices.max())
        
        drawdown = (max_price - current_price) / max_price
        return drawdown

    def evaluate_signal(self, signal: SignalOutput) -> RiskOutput:
        # 1. Check Conviction Score
        if signal.conviction < self.min_conviction:
            return RiskOutput(signal=signal, approved=False, veto_reason=f"VETO: Conviction score ({signal.conviction}) too low.", risk_multiplier=0.0)
            
        if signal.direction == "FLAT":
             return RiskOutput(signal=signal, approved=False, veto_reason="VETO: Signal direction is FLAT.", risk_multiplier=0.0)

        # 2. Check VIX Regime & Set Risk Multiplier
        vix = self.get_vix_for_date(signal.date)
        if vix > self.max_vix:
            return RiskOutput(signal=signal, approved=False, veto_reason=f"VETO: Market VIX ({vix:.2f}) exceeds max threshold.", risk_multiplier=0.0)
            
        risk_multiplier = 1.0
        if vix > 20.0:
            risk_multiplier = 0.5  # Cut position size in half if VIX is elevated
            vix_reason = f"Elevated VIX ({vix:.2f}) -> Half Size"
        else:
            vix_reason = f"Calm VIX ({vix:.2f}) -> Full Size"
            
        # 3. Check Asset Drawdown (Catching falling knives)
        # If the asset has dropped more than max_drawdown in the last 30 days, going LONG is risky.
        drawdown = self.get_asset_drawdown(signal.date)
        if drawdown > self.max_drawdown and signal.direction == "LONG":
            # Heavily penalize the risk multiplier for catching a falling knife
            risk_multiplier *= 0.5
            dd_reason = f"Severe Drawdown ({drawdown*100:.1f}%) -> Penalty applied."
        else:
            dd_reason = f"Healthy Price Action (DD: {drawdown*100:.1f}%)."

        final_reason = f"APPROVED. {vix_reason}. {dd_reason}"

        return RiskOutput(
            signal=signal, 
            approved=True, 
            veto_reason=final_reason,
            risk_multiplier=risk_multiplier
        )
