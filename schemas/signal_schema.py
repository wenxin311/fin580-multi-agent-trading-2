"""
Signal Schema for Agent 3

Purpose:
Defines structured trading signals,
historical analog comparisons,
and preliminary alpha evaluation.
"""

from pydantic import BaseModel


class SignalOutput(BaseModel):

    # Reference event
    event_id: str

    # Tradable asset
    asset: str

    # Market ticker
    ticker: str

    # Trading direction
    signal: str

    # Signal strength
    signal_strength: float

    # Conviction score
    conviction_score: int

    # Suggested entry timing
    entry_timing: str

    # Suggested holding period
    holding_period_days: int

    # Trading rationale
    supporting_reason: str

    # -----------------------------------
    # Mini Backtest Metrics
    # -----------------------------------

    # Historical average return
    historical_avg_return: float

    # Historical win rate
    historical_win_rate: float

    # Expected alpha estimate
    expected_alpha: float

    # -----------------------------------
    # Historical Analog Reasoning
    # -----------------------------------

    # Most similar historical event
    historical_analog_event: str

    # Historical return of analog event
    historical_analog_return: float

    # Similarity score
    historical_similarity_score: float