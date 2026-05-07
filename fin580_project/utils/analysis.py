import pandas as pd

def analyze_conviction(df):
    df = df.copy()

    # Remove NaN
    df = df.dropna(subset=["strategy_return"])

    # Group by conviction
    result = df.groupby("conviction")["strategy_return"].mean()

    print("\nAverage Return by Conviction:")
    print(result)

    return result
def analyze_event_performance(df):
    df = df.copy()

    # remove NaN returns
    df = df.dropna(subset=["strategy_return"])

    result = df.groupby("event_type")["strategy_return"].mean()

    print("\nAverage Return by Event Type:")
    print(result)

    return result