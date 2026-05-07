"""
Agent 5 — Portfolio Manager Agent

Purpose:
This agent converts approved trading signals
into executable portfolio positions.

Main Responsibilities:
1. Determine final position sizing
2. Generate executable trade decisions
3. Create portfolio audit trails
4. Simulate institutional portfolio construction

Current Version:
Mock Development Mode
"""

from schemas.portfolio_schema import PortfolioOutput


def run_portfolio_agent(signal_output, risk_output):

    """
    Simulates final portfolio construction.

    Input:
    - Signal output from Agent 3
    - Risk output from Agent 4

    Output:
    - Final executable portfolio decision
    """

    # Base portfolio capital
    portfolio_capital = 1_000_000

    # Position sizing logic
    final_position_size = int(
        portfolio_capital
        * 0.30
        * risk_output.position_multiplier
    )

    portfolio = PortfolioOutput(

        event_id=signal_output.event_id,

        final_decision="EXECUTE",

        final_position=signal_output.signal,

        ticker=signal_output.ticker,

        position_size_usd=final_position_size,

        entry_price_reference=82.35,

        expected_holding_period=signal_output.holding_period_days,

        execution_timestamp="2024-05-01 09:31:00",

        portfolio_reasoning=(
            "Bullish Brent thesis approved by risk manager. "
            "Position size reduced under high volatility regime."
        )
    )

    return portfolio