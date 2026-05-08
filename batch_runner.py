"""
Batch Pipeline Runner

Purpose:
Run the A3 → A5 trading pipeline
using processed A1/A2 outputs.

Features:
- Batch signal generation
- Risk evaluation
- Portfolio execution
- Latency tracking
- API cost estimation
"""

import json
import time
import pandas as pd

from agents.signal_agent import run_signal_agent
from agents.risk_agent import RiskManagerAgent
from agents.portfolio_agent import PortfolioManagerAgent


# -----------------------------------
# API Cost Assumptions
# -----------------------------------

TOKEN_COST_PER_1K = 0.01

AVG_AGENT_TOKEN_USAGE = {

    "A3": 600,

    "A4": 400,

    "A5": 300
}


# -----------------------------------
# Load A1 + A2 Outputs
# -----------------------------------

with open(

    "data/processed/a1_a2_merged.json",

    "r"

) as f:

    events = json.load(f)


# -----------------------------------
# Initialize Agents
# -----------------------------------

risk_agent = RiskManagerAgent()

portfolio_agent = PortfolioManagerAgent()


# -----------------------------------
# Store Results
# -----------------------------------

results = []

latency_results = []

api_cost_results = []


# -----------------------------------
# Run Pipeline
# -----------------------------------

for e in events:

    print("\n==============================")

    print("Processing Event:")

    print(e["event_type"])


    # ===================================
    # Agent 3 — Signal Generation
    # ===================================

    start = time.time()

    signal_output = run_signal_agent(e)

    a3_latency = time.time() - start


    # ===================================
    # Agent 4 — Risk Management
    # ===================================

    start = time.time()

    risk_output = risk_agent.evaluate_signal(
        signal_output
    )

    a4_latency = time.time() - start


    # ===================================
    # Agent 5 — Portfolio Execution
    # ===================================

    start = time.time()

    portfolio_output = portfolio_agent.execute_trade(
        risk_output
    )

    a5_latency = time.time() - start


    # -----------------------------------
    # Save Final Results
    # -----------------------------------

    results.append({

        "event_id":
            signal_output.event_id,

        "event_type":
             e["event_type"],

        "signal":
            signal_output.signal,

        "conviction":
            signal_output.conviction_score,

        "holding_days":
            signal_output.holding_period_days,

        "expected_alpha":
            signal_output.expected_alpha,

        "approved":
            risk_output.approved,

        "position":
            portfolio_output.direction,

        "position_size":
            portfolio_output.size_usd
    })


    # -----------------------------------
    # API Cost Estimation
    # -----------------------------------

    total_tokens = (

        AVG_AGENT_TOKEN_USAGE["A3"]
        + AVG_AGENT_TOKEN_USAGE["A4"]
        + AVG_AGENT_TOKEN_USAGE["A5"]
    )

    estimated_cost = (

        total_tokens / 1000
    ) * TOKEN_COST_PER_1K


    api_cost_results.append({

        "event_id":
            signal_output.event_id,

        "estimated_tokens":
            total_tokens,

        "estimated_cost_usd":
            estimated_cost
    })


    # -----------------------------------
    # Latency Tracking
    # -----------------------------------

    latency_results.append({

        "event_id":
            signal_output.event_id,

        "A3_latency":
            a3_latency,

        "A4_latency":
            a4_latency,

        "A5_latency":
            a5_latency,

        "total_latency":

            a3_latency
            + a4_latency
            + a5_latency
    })


# -----------------------------------
# Save Outputs
# -----------------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(

    "outputs/batch_results.csv",

    index=False
)


api_cost_df = pd.DataFrame(
    api_cost_results
)

api_cost_df.to_csv(

    "outputs/api_costs.csv",

    index=False
)


latency_df = pd.DataFrame(
    latency_results
)

latency_df.to_csv(

    "outputs/latency_results.csv",

    index=False
)


# -----------------------------------
# Completion Message
# -----------------------------------

print("\nBatch testing complete.")

print("\nSaved files:")

print("outputs/batch_results.csv")

print("outputs/latency_results.csv")

print("outputs/api_costs.csv")