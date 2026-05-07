"""
Agent 3 — Signal / Asset Mapping Agent

Purpose:
This agent converts macroeconomic reasoning
into actionable trading signals.

Main Responsibilities:
1. Generate LONG / SHORT / FLAT signals
2. Estimate signal strength
3. Define holding horizon
4. Create explainable trading rationale

Current Version:
Mock Development Mode
"""

from schemas.signal_schema import SignalOutput


def run_signal_agent(macro_output):

    """
    Simulates signal generation
    based on macroeconomic interpretation.

    Input:
    - Structured macro output from Agent 2

    Output:
    - Structured trading signal
    """

    signal = SignalOutput(

        event_id=macro_output.event_id,

        asset="Brent Crude Oil",

        ticker="BZ=F",

        signal="LONG",

        signal_strength=0.84,

        conviction_score=5,

        entry_timing="Next Market Open",

        holding_period_days=7,

        supporting_reason=(
            "Supply tightening is expected "
            "to increase upward pressure on Brent prices."
        )
    )

    return signal