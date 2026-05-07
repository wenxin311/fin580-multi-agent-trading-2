import json
import pandas as pd
from agents.signal_agent import SignalAgent
from backtest.backtester import Backtester
from utils.fake_price import generate_fake_prices
from utils.plot import plot_cumulative_return
from utils.analysis import analyze_conviction, analyze_event_performance
from agents.random_agent import RandomAgent
from agents.no_conviction_agent import NoConvictionAgent
from agents.no_event_agent import NoEventAgent
from agents.single_agent import SingleAgent

# Load events
with open("data/mock_data.json", "r") as f:
    events = json.load(f)

events_df = pd.DataFrame(events)

# Initialize
agent = SignalAgent()
bt = Backtester()

# 🔥 Pipeline
def run_pipeline(events_subset, agent):
    API_COST_PER_CALL = 0.001

    signals = []
    api_calls = 0

    for _, event in events_subset.iterrows():
        signal = agent.generate_signal(event)
        signals.append(signal)
        api_calls += 1

    prices = generate_fake_prices(len(signals))
    result_df = bt.run(signals, prices)

    total_api_cost = api_calls * API_COST_PER_CALL
    print(f"API Cost: ${total_api_cost:.4f}")

    return result_df


# =====================
# 🥇 A3 MAIN STRATEGY
# =====================
print("\n=== A3 Strategy (Full Sample) ===")
a3_df = run_pipeline(events_df, agent)

a3_df.to_csv("data/backtest_results.csv", index=False)

plot_cumulative_return(a3_df)
analyze_conviction(a3_df)
analyze_event_performance(a3_df)


# =====================
# 🥈 BASELINE & ABLATION
# =====================
print("\n=== Random Baseline ===")
random_df = run_pipeline(events_df, RandomAgent())

print("\n=== No Conviction ===")
no_conv_df = run_pipeline(events_df, NoConvictionAgent())

print("\n=== No Event ===")
no_event_df = run_pipeline(events_df, NoEventAgent())


# =====================
# 🥉 OUT-OF-SAMPLE
# =====================
split_idx = int(len(events_df) * 0.7)

train_events = events_df.iloc[:split_idx]
test_events = events_df.iloc[split_idx:]

print("\n=== TRAIN (A3) ===")
train_df = run_pipeline(train_events, agent)

print("\n=== TEST (A3) ===")
test_df = run_pipeline(test_events, agent)

print("\n=== Single Agent Baseline ===")
single_df = run_pipeline(events_df, SingleAgent())