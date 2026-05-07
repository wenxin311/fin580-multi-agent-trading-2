"""
Agent 1 — Event Detection Agent

Purpose:
This agent converts raw financial news into
structured macroeconomic event data.

Main Responsibilities:
1. Detect important macro events
2. Extract entities
3. Classify event type
4. Estimate directional impact on Brent oil

Current Version:
Mock Development Mode (No OpenAI API yet)

Why mock mode?
We first validate the architecture and agent pipeline
before connecting live LLM inference.
"""

from schemas.event_schema import EventOutput


def run_event_agent(news_text: str, timestamp: str):

    """
    Simulates event detection from raw news text.

    Input:
    - news_text: raw financial news headline or article
    - timestamp: publication timestamp

    Output:
    - Structured EventOutput object
    """

    # Mock structured event output
    event = EventOutput(

        event_id="EVT_001",

        timestamp=timestamp,

        headline=news_text,

        event_type="Supply Shock",

        category="Energy Policy",

        entities=[
            "OPEC",
            "Saudi Arabia"
        ],

        directional_bias="Bullish Brent",

        confidence_score=0.91,

        source="Reuters"
    )

    return event