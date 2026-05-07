"""
Agent 4 — Risk Management Agent

Purpose:
This agent evaluates whether a trading signal
should be approved, resized, or rejected
based on current market risk conditions.

Main Responsibilities:
1. Assess volatility regime
2. Control position sizing
3. Enforce drawdown constraints
4. Approve or veto trades

Current Version:
Mock Development Mode
"""

from schemas.risk_schema import RiskOutput


def run_risk_agent(signal_output):

    """
    Simulates institutional risk management.

    Input:
    - Structured signal output from Agent 3

    Output:
    - Structured risk management decision
    """

    risk = RiskOutput(

        event_id=signal_output.event_id,

        risk_approval=True,

        risk_regime="High Volatility",

        vix_level=28,

        position_multiplier=0.5,

        max_drawdown_check="PASS",

        turnover_check="PASS",

        risk_notes=(
            "Position size reduced due to elevated "
            "market volatility conditions."
        )
    )

    return risk