"""
Macro Schema for Agent 2

Purpose:
Defines structured macroeconomic reasoning
generated from detected events.
"""

from pydantic import BaseModel


class MacroOutput(BaseModel):

    # Reference to original event
    event_id: str

    # Macroeconomic interpretation
    macro_thesis: str

    # Narrative sentiment score
    sentiment_score: float