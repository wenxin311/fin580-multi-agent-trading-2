"""
Portfolio Schema for Agent 5 (Portfolio Manager Agent)

Purpose:
This schema defines the final executable portfolio
decision generated after signal and risk evaluation.

Why this matters:
- Converts approved signals into final trades
- Produces position sizing decisions
- Creates a full audit trail
- Enables backtesting and execution simulation
"""

from pydantic import BaseModel


class PortfolioOutput(BaseModel):

    # Reference to original event
    event_id: str

    # Final execution decision
    final_decision: str

    # Final trading direction
    final_position: str

    # Target asset ticker
    ticker: str

    # Final USD position size
    position_size_usd: int

    # Reference entry price
    entry_price_reference: float

    # Expected holding duration
    expected_holding_period: int

    # Simulated execution timestamp
    execution_timestamp: str

    # Final portfolio reasoning
    portfolio_reasoning: str