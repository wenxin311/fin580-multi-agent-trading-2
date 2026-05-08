"""
Main Pipeline Runner

Purpose:
Test the full end-to-end execution
of the multi-agent trading system.
"""

from agents.event_agent import run_event_agent
from agents.macro_agent import run_macro_agent
from agents.signal_agent import run_signal_agent
from agents.risk_agent import run_risk_agent
from agents.portfolio_agent import run_portfolio_agent


# ---------------------------------------------------
# SAMPLE NEWS INPUT
# ---------------------------------------------------

sample_news = """
OPEC announced a surprise production cut
of 1 million barrels per day.
"""

sample_timestamp = "2024-05-01 08:30:00"


# ---------------------------------------------------
# AGENT 1 — EVENT DETECTION
# ---------------------------------------------------

event_output = run_event_agent(
    sample_news,
    sample_timestamp
)


# ---------------------------------------------------
# AGENT 2 — MACRO REASONING
# ---------------------------------------------------

macro_output = run_macro_agent(event_output)


# ---------------------------------------------------
# AGENT 3 — SIGNAL GENERATION
# ---------------------------------------------------

signal_output = run_signal_agent(macro_output)


# ---------------------------------------------------
# AGENT 4 — RISK MANAGEMENT
# ---------------------------------------------------

risk_output = run_risk_agent(signal_output)


# ---------------------------------------------------
# AGENT 5 — PORTFOLIO CONSTRUCTION
# ---------------------------------------------------

portfolio_output = run_portfolio_agent(risk_output)


# ---------------------------------------------------
# PRINT OUTPUTS
# ---------------------------------------------------

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