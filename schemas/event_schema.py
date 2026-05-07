"""
Event Schema for Agent 1 (Event Detection Agent)

Purpose:
This schema defines the structured output format
for all detected macroeconomic and geopolitical events.

Why this matters:
- Standardizes communication between agents
- Enables auditability and reproducibility
- Prevents malformed JSON outputs
- Creates structured event records for downstream agents
"""

from pydantic import BaseModel
from typing import List


class EventOutput(BaseModel):

    # Unique event identifier
    event_id: str

    # Original publication timestamp
    timestamp: str

    # Original news headline
    headline: str

    # High-level event classification
    event_type: str

    # Event category
    category: str

    # Key organizations, countries, or institutions
    entities: List[str]

    # Expected directional impact on Brent oil
    directional_bias: str

    # Confidence score between 0 and 1
    confidence_score: float

    # News source
    source: str