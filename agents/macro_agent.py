"""
Agent 2 — Macro Transmission Agent

Purpose:
This agent converts structured events into
macroeconomic interpretations and market reasoning.

Main Responsibilities:
1. Interpret macroeconomic implications
2. Build causal reasoning chains
3. Estimate oil market impact
4. Generate structured macro thesis

Current Version:
Mock Development Mode
"""

from schemas.macro_schema import MacroOutput


def run_macro_agent(event_output):

    """
    Simulates macroeconomic reasoning
    based on detected events.

    Input:
    - Structured event output from Agent 1

    Output:
    - Structured macro interpretation
    """

    macro = MacroOutput(

        event_id=event_output.event_id,

        macro_thesis=(
            "OPEC production cuts are expected "
            "to tighten global crude supply and "
            "increase upward pressure on Brent prices."
        ),

        causal_chain=[
            "Production cuts reduce global oil supply",
            "Lower inventories tighten energy markets",
            "Supply-demand imbalance pushes prices higher"
        ],

        affected_factors=[
            "Global Oil Supply",
            "Oil Inventories",
            "Energy Inflation"
        ],

        market_regime="Inflationary",

        expected_impact="Bullish Brent",

        conviction_score=4,

        time_horizon="Medium-term"
    )

    return macro