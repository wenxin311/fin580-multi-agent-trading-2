import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, initial_capital=1_000_000, latency=1):
        self.initial_capital = initial_capital
        self.latency = latency

    def run(self, signals, prices):
        df = pd.DataFrame(signals)

        # Price and returns
        df["price"] = prices
        df["returns"] = df["price"].pct_change()

        # Map signal to position
        df["position"] = df["signal"].map({
            "LONG": 1,
            "SHORT": -1,
            "FLAT": 0
        })

        # ✅ Apply latency (ONLY ONCE)
        df["position"] = df["position"].shift(self.latency)
        df["position_size"] = (df["conviction"] / 5).shift(self.latency)

        # Transaction cost (30 bps)
        cost = 0.003

        df["trade"] = df["position"].diff().abs()
        df["transaction_cost"] = df["trade"] * cost

        # Strategy return
        df["strategy_return"] = (
            df["position"] *
            df["position_size"] *
            df["returns"]
        ) - df["transaction_cost"]

        # Cumulative return
        df["cumulative_return"] = (1 + df["strategy_return"]).cumprod()

        # Metrics
        mean_return = df["strategy_return"].mean()
        volatility = df["strategy_return"].std()
        sharpe = mean_return / volatility if volatility != 0 else 0

        rolling_max = df["cumulative_return"].cummax()
        drawdown = df["cumulative_return"] / rolling_max - 1
        max_drawdown = drawdown.min()

        win_rate = (df["strategy_return"] > 0).sum() / df["strategy_return"].count()
        total_return = df["cumulative_return"].iloc[-1] - 1

        print("Total Return:", round(total_return, 4))
        print("Sharpe Ratio:", round(sharpe, 4))
        print("Volatility:", round(volatility, 4))
        print("Max Drawdown:", round(max_drawdown, 4))
        print("Win Rate:", round(win_rate, 4))

        return df