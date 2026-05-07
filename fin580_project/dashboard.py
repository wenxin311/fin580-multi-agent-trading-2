import streamlit as st
import pandas as pd

# Load results
df = pd.read_csv("data/backtest_results.csv")

st.title("Trading Strategy Dashboard")

# Metrics
st.subheader("Performance Metrics")

total_return = df["cumulative_return"].iloc[-1] - 1
st.write(f"Total Return: {total_return:.2%}")

# Plot
st.subheader("Cumulative Return")
st.line_chart(df["cumulative_return"])

# Conviction analysis
st.subheader("Conviction Analysis")
conviction_perf = df.groupby("conviction")["strategy_return"].mean()
st.bar_chart(conviction_perf)

# Event analysis
st.subheader("Event Type Analysis")
event_perf = df.groupby("event_type")["strategy_return"].mean()
st.bar_chart(event_perf)

sharpe = df["strategy_return"].mean() / df["strategy_return"].std()
max_dd = (df["cumulative_return"] / df["cumulative_return"].cummax() - 1).min()

st.write(f"Sharpe Ratio: {sharpe:.2f}")
st.write(f"Max Drawdown: {max_dd:.2%}")