from schemas.risk_schema import RiskOutput
from schemas.portfolio_schema import PortfolioOutput
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

class PortfolioManagerAgent:
    def __init__(self, initial_capital=1000000.0, max_position_pct=0.10, min_cash_buffer_pct=0.15):
        # Requirements: $1,000,000 initial capital
        self.total_portfolio_value = initial_capital
        
        # Integration of IRL Portfolio Holdings
        # These represent the "Static" part of the Roth-IRA that Agent 5 protects.
        self.core_holdings = {
            "FXAIX": "Fidelity 500 Index",
            "FZROX": "Fidelity Total Market",
            "BRK-B": "Berkshire Hathaway",
            "GOOG": "Alphabet",
            "VRT": "Vertiv Holdings",
            "GBX": "Greenbrier Companies",
            "MAIN": "Main Street Capital",
            "WSM": "Williams-Sonoma",
            "BF-A": "Brown-Forman"
        }
        
        # We simulate that 80% is locked in these core holdings
        self.allocated_in_core = initial_capital * 0.80
        self.available_cash = initial_capital - self.allocated_in_core
        
        self.max_position_pct = max_position_pct
        # Defensive Roth IRA style rule: Always maintain a strict minimum cash buffer
        self.min_cash_buffer_pct = min_cash_buffer_pct 
        self.portfolio_log = []
        
    def get_entry_price(self, date_str: str) -> float:
        # Fetch real entry price for BZ=F
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            data = yf.download("BZ=F", start=(target_date - timedelta(days=7)).strftime("%Y-%m-%d"), end=(target_date + timedelta(days=1)).strftime("%Y-%m-%d"), progress=False)
            if not data.empty:
                if isinstance(data.columns, pd.MultiIndex):
                    return float(data['Close']['BZ=F'].iloc[-1])
                return float(data['Close'].iloc[-1])
        except Exception:
            pass
        return 80.0
        
    def size_trade(self, risk_decision: RiskOutput) -> PortfolioOutput:
        if not risk_decision.approved:
            return None
            
        signal = risk_decision.signal
        
        # 1. Base allocation based on Conviction (e.g. 5/5 = 100% of max allowed position)
        base_allocation_pct = (signal.conviction / 5.0) * self.max_position_pct
        
        # 2. Apply the dynamic risk multiplier from Agent 4
        final_allocation_pct = base_allocation_pct * risk_decision.risk_multiplier
        intended_trade_size = self.total_portfolio_value * final_allocation_pct
        
        # 3. Roth IRA Cash Buffer Constraint
        # A defensive retirement portfolio must never dip below its minimum cash reserve.
        min_required_cash = self.total_portfolio_value * self.min_cash_buffer_pct
        max_deployable_cash = self.available_cash - min_required_cash
        
        if max_deployable_cash <= 0:
            print(f"   [PORTFOLIO VETO] Trade Rejected. Available cash (${self.available_cash:,.2f}) has hit the absolute minimum buffer reserve.")
            return None
            
        # Cap the trade size to whatever deployable cash we have left
        actual_trade_size = min(intended_trade_size, max_deployable_cash)
        
        # 4. Deduct from available cash (For a real backtester, Student B will add cash back when trades are closed)
        self.available_cash -= actual_trade_size
        
        entry_price = self.get_entry_price(signal.date)
        
        # Formatting the reasoning trace to show the math
        cash_note = ""
        if actual_trade_size < intended_trade_size:
            cash_note = f" (NOTE: Capped by Cash Buffer - Reduced from ${intended_trade_size:,.0f} to ${actual_trade_size:,.0f})"
            
        trace = f"A4 Risk Multiplier: {risk_decision.risk_multiplier}x. A5 Sizing: Allocated {final_allocation_pct*100:.1f}%{cash_note}. Cash remaining: ${self.available_cash:,.0f}."
        
        trade = PortfolioOutput(
            date=signal.date,
            asset=signal.asset,
            direction=signal.direction,
            size_usd=actual_trade_size,
            entry_price_ref=entry_price,
            reasoning_trace=trace
        )
        self.portfolio_log.append(trade)
        return trade
