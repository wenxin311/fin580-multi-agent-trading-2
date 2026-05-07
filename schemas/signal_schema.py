##Structured Trading Decision Layer##

"""
Signal Schema for Agent 3 (Signal / Asset Mapping Agent)

Purpose:
This schema defines the structured trading signal
generated from macroeconomic reasoning outputs.

Why this matters:
- Converts macro reasoning into tradable signals
- Standardizes signal generation
- Enables downstream risk management
- Creates explainable portfolio actions
"""

from pydantic import BaseModel


class SignalOutput(BaseModel):

    # Reference to original event
    event_id: str

    # Target tradable asset
    asset: str

    # Market ticker
    ticker: str

    # Trading direction
    signal: str

    # Quantitative signal strength
    signal_strength: float

    # Qualitative conviction score
    conviction_score: int

    # Suggested entry timing
    entry_timing: str

    # Suggested holding horizon
    holding_period_days: int

    # Supporting reasoning
    supporting_reason: str