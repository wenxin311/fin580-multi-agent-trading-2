"""
Backtest Engine

Purpose:
Run historical backtesting with:

- Train/Test split
- Out-of-sample evaluation
- Sharpe ratio
- Max drawdown
"""

import pandas as pd

from backtest.trade_simulator import TradeSimulator
from backtest.performance_metrics import PerformanceMetrics


# -----------------------------------
# Load Historical Brent Prices
# -----------------------------------

prices = pd.read_csv(

    "data/brent_prices.csv"
)


# -----------------------------------
# Clean Dataset
# -----------------------------------

# Rename first column to Date
prices.rename(

    columns={prices.columns[0]: "Date"},

    inplace=True
)

# Convert Date column
prices["Date"] = pd.to_datetime(
    prices["Date"],
    errors="coerce"
)

# Remove invalid rows
prices = prices.dropna(
    subset=["Date"]
)

# Set datetime index
prices = prices.set_index("Date")

# Sort index
prices = prices.sort_index()


# -----------------------------------
# Train / Test Split
# -----------------------------------

train_prices = prices[

    (prices.index >= "2020-01-01")
    &
    (prices.index <= "2022-12-31")
]

test_prices = prices[

    (prices.index >= "2023-01-01")
    &
    (prices.index <= "2024-12-31")
]


# -----------------------------------
# Initialize Simulators
# -----------------------------------

train_simulator = TradeSimulator(
    train_prices
)

test_simulator = TradeSimulator(
    test_prices
)


# -----------------------------------
# Train Signals
# -----------------------------------

train_signals = [

    {
        "date": "2020-06-01",
        "signal": "LONG",
        "holding_days": 7
    },

    {
        "date": "2021-03-15",
        "signal": "LONG",
        "holding_days": 10
    }
]


# -----------------------------------
# Test Signals
# -----------------------------------

test_signals = [

    {
        "date": "2023-05-01",
        "signal": "LONG",
        "holding_days": 7
    },

    {
        "date": "2024-02-15",
        "signal": "SHORT",
        "holding_days": 5
    }
]


# -----------------------------------
# Run Train Simulations
# -----------------------------------

for s in train_signals:

    train_simulator.simulate_trade(

        signal=s["signal"],

        entry_date=pd.to_datetime(
            s["date"]
        ),

        holding_days=s["holding_days"]
    )


# -----------------------------------
# Run Test Simulations
# -----------------------------------

for s in test_signals:

    test_simulator.simulate_trade(

        signal=s["signal"],

        entry_date=pd.to_datetime(
            s["date"]
        ),

        holding_days=s["holding_days"]
    )


# -----------------------------------
# Train Results
# -----------------------------------

train_returns = [

    t["net_return"]

    for t in train_simulator.trade_history
]

train_capital_curve = [

    t["capital"]

    for t in train_simulator.trade_history
]


# -----------------------------------
# Test Results
# -----------------------------------

test_returns = [

    t["net_return"]

    for t in test_simulator.trade_history
]

test_capital_curve = [

    t["capital"]

    for t in test_simulator.trade_history
]


# -----------------------------------
# Train Metrics
# -----------------------------------

train_sharpe = PerformanceMetrics.sharpe_ratio(
    train_returns
)

train_drawdown = PerformanceMetrics.max_drawdown(
    train_capital_curve
)


# -----------------------------------
# Test Metrics
# -----------------------------------

test_sharpe = PerformanceMetrics.sharpe_ratio(
    test_returns
)

test_drawdown = PerformanceMetrics.max_drawdown(
    test_capital_curve
)


# -----------------------------------
# Print Results
# -----------------------------------

print("\n===== TRAIN RESULTS =====")

print(
    f"Train Sharpe Ratio: "
    f"{train_sharpe:.2f}"
)

print(
    f"Train Max Drawdown: "
    f"{train_drawdown:.2%}"
)


print("\n===== TEST RESULTS =====")

print(
    f"Test Sharpe Ratio: "
    f"{test_sharpe:.2f}"
)

print(
    f"Test Max Drawdown: "
    f"{test_drawdown:.2%}"
)