"""
Portfolio Schema for Agent 5

Purpose:
Defines executable portfolio trades
generated after risk approval.
"""

from pydantic import BaseModel


class PortfolioOutput(BaseModel):

    # Trade date
    date: str

    # Tradable asset
    asset: str

    # Trading direction
    direction: str

    # USD trade size
    size_usd: float

    # Reference entry price
    entry_price_ref: float

    # Explainable reasoning trace
    reasoning_trace: str