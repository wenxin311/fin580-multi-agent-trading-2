## Explainable Macro Reasoning Structure##

"""
Macro Schema for Agent 2 (Macro Transmission Agent)

Purpose:
This schema defines the structured macroeconomic
reasoning output generated from detected events.

Why this matters:
- Converts raw events into economic interpretation
- Creates explainable causal reasoning chains
- Standardizes macro thesis generation
- Enables downstream trading signal generation
"""

from pydantic import BaseModel
from typing import List


class MacroOutput(BaseModel):

    # Reference to original event
    event_id: str

    # High-level macro thesis
    macro_thesis: str

    # Step-by-step causal reasoning
    causal_chain: List[str]

    # Key affected macro factors
    affected_factors: List[str]

    # Current macro regime
    market_regime: str

    # Expected directional impact
    expected_impact: str

    # Confidence / conviction score
    conviction_score: int

    # Expected time horizon
    time_horizon: str