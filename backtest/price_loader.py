"""
Price Loader

Purpose:
Download historical Brent crude prices.
"""

import yfinance as yf
import pandas as pd


def download_brent_prices():

    # Download Brent futures data
    data = yf.download(

        "BZ=F",

        start="2020-01-01",

        end="2025-01-01",

        auto_adjust=True
    )

    # Keep only Close prices
    data = data[["Close"]]

    # Reset clean index
    data.reset_index(inplace=True)

    # Save clean CSV
    data.to_csv(

        "data/brent_prices.csv",

        index=False
    )

    print("Brent price data saved.")


if __name__ == "__main__":

    download_brent_prices()