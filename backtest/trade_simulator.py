"""
Trade Simulator

Purpose:
Simulate trading performance using
Agent 3 signals.

Features:
- LONG / SHORT simulation
- Transaction cost modeling
- Portfolio capital tracking
- Trade history logging
"""

import pandas as pd


# -----------------------------------
# Global Backtest Settings
# -----------------------------------

TRANSACTION_COST = 0.003     # 30 bps
INITIAL_CAPITAL = 1_000_000  # $1M


class TradeSimulator:

    def __init__(self, price_data):

        """
        Initialize simulator.

        Inputs:
        - Historical price dataframe
        """

        self.price_data = price_data
        self.capital = INITIAL_CAPITAL
        self.trade_history = []

    def simulate_trade(
        self,
        signal,
        entry_date,
        holding_days
    ):

        """
        Simulate a single trade.

        Inputs:
        - signal: LONG / SHORT / FLAT
        - entry_date: trade entry date
        - holding_days: holding horizon

        Output:
        - Structured trade result
        """

        # -----------------------------------
        # Validate entry date
        # -----------------------------------

        if entry_date not in self.price_data.index:

            print(f"Missing date: {entry_date}")

            return None

        # -----------------------------------
        # Load entry price
        # -----------------------------------

        entry_price = float(
            self.price_data.loc[entry_date]["Close"]
        )

        # -----------------------------------
        # Calculate exit index
        # -----------------------------------

        exit_index = (
            self.price_data.index.get_loc(entry_date)
            + holding_days
        )

        # Prevent out-of-range errors
        if exit_index >= len(self.price_data):

            print("Exit index exceeds dataset.")

            return None

        # -----------------------------------
        # Load exit price
        # -----------------------------------

        exit_date = self.price_data.index[exit_index]

        exit_price = float(
            self.price_data.loc[exit_date]["Close"]
        )

        # -----------------------------------
        # Calculate trade return
        # -----------------------------------

        if signal == "LONG":

            gross_return = (
                exit_price - entry_price
            ) / entry_price

        elif signal == "SHORT":

            gross_return = (
                entry_price - exit_price
            ) / entry_price

        else:

            gross_return = 0

        # -----------------------------------
        # Apply transaction cost
        # -----------------------------------

        net_return = (
            gross_return - TRANSACTION_COST
        )

        # -----------------------------------
        # Calculate PnL
        # -----------------------------------

        pnl = self.capital * net_return

        # Update portfolio capital
        self.capital += pnl

        # -----------------------------------
        # Save trade result
        # -----------------------------------

        trade_result = {

            "entry_date": str(entry_date),

            "exit_date": str(exit_date),

            "signal": signal,

            "entry_price": float(entry_price),

            "exit_price": float(exit_price),

            "gross_return": float(gross_return),

            "net_return": float(net_return),

            "pnl": float(pnl),

            "capital": float(self.capital)
        }

        # Store trade history
        self.trade_history.append(trade_result)

        return trade_result