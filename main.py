"""
Main Pipeline Runner

Purpose:
This file tests the end-to-end execution
of the multi-agent architecture.

Current Stage:
Testing Agent 1 (Event Detection Agent)
"""

from agents.event_agent import run_event_agent
from agents.macro_agent import run_macro_agent
from agents.signal_agent import run_signal_agent
from agents.risk_agent import run_risk_agent
from agents.portfolio_agent import run_portfolio_agent

# Example financial news
sample_news = """
OPEC announced a surprise production cut
of 1 million barrels per day.
"""

# Example timestamp
sample_timestamp = "2024-05-01 08:30:00"


# Run Agent 1
event_output = run_event_agent(
    sample_news,
    sample_timestamp
)

# Run Agent 2
macro_output = run_macro_agent(event_output)

# Run Agent 3
signal_output = run_signal_agent(macro_output)

# Run Agent 4
risk_output = run_risk_agent(signal_output)

# Run Agent 5
portfolio_output = run_portfolio_agent(
    signal_output,
    risk_output
)


# Print structured result
print("\n===== EVENT OUTPUT =====")
print(event_output.model_dump_json(indent=4))

print("\n===== MACRO OUTPUT =====")
print(macro_output.model_dump_json(indent=4))

print("\n===== SIGNAL OUTPUT =====")
print(signal_output.model_dump_json(indent=4))

print("\n===== RISK OUTPUT =====")
print(risk_output.model_dump_json(indent=4))

print("\n===== PORTFOLIO OUTPUT =====")
print(portfolio_output.model_dump_json(indent=4))