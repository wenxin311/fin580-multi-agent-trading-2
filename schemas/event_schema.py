"""
Event Schema for Agent 1

Purpose:
Defines structured event outputs
generated from financial news.
"""

from pydantic import BaseModel
from typing import List


class EventOutput(BaseModel):

    # Unique event identifier
    event_id: str

    # News timestamp
    timestamp: str

    # Event classification
    event_type: str

    # Relevant entities
    entities: List[str]

    # Model confidence score
    confidence: float