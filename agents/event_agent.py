"""
==============================================================================
  AGENT 1 -- EVENT DETECTION & CLASSIFICATION (Student A)
  FIN580 Quantamental Investment Project -- Brent Crude Oil
==============================================================================
  This agent processes raw news articles and outputs structured event objects.

  Pipeline:
    1. Load news data (from mock JSON or live API)
    2. Run FinBERT sentiment analysis on each headline
    3. Extract named entities via spaCy NER
    4. Call Gemini LLM for event classification (type, bias, confidence)
    5. Save structured events to data/processed/a1_events.json

  Usage:
    python agent1_event_detection.py

  Output:
    data/processed/a1_events.json  ->  consumed by Agent 2
==============================================================================
"""

import os
import uuid
import json
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional

# ── Local NLP Models ────────────────────────────────────────────────────────
import spacy
from transformers import pipeline as hf_pipeline

# ── Gemini SDK ──────────────────────────────────────────────────────────────
from google import genai
from google.genai import types

# ============================================================================
#  CONFIGURATION
# ============================================================================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL   = "gemini-2.5-flash"
FINBERT_MODEL  = "ProsusAI/finbert"
SPACY_MODEL    = "en_core_web_sm"
MOCK_MODE      = True           # Set True to skip all API calls
RATE_LIMIT_SEC = 2              # Seconds to sleep between articles (paid tier)

# ============================================================================
#  SCHEMA — EventOutput
# ============================================================================
class EventOutput(BaseModel):
    event_id: str
    timestamp: str
    headline: str
    event_type: str
    category: str
    entities: List[str]
    directional_bias: str
    confidence_score: float
    source: str
    sentiment_score: Optional[float] = None
    raw_text: Optional[str] = None
    processing_timestamp: Optional[str] = None

# ============================================================================
#  DATA LOADER — MockNewsScraper
# ============================================================================
class MockNewsScraper:
    def __init__(self, data_path: str = "fin580_project/data/mock_data.json"):
        self.data_path = data_path

    def fetch_news(self) -> list:
        """Load mock news articles from the local JSON file."""
        try:
            with open(self.data_path, "r") as f:
                raw_data = json.load(f)
            formatted = []
            for item in raw_data:
                formatted.append({
                    "headline": item.get("macro_thesis", "Unknown Event")
                                + " relating to "
                                + ", ".join(item.get("entities", [])),
                    "source": "Mock DB",
                    "timestamp": item.get("timestamp", "2024-01-01T00:00:00Z"),
                })
            print(f"[Agent 1] Loaded {len(formatted)} articles from {self.data_path}")
            return formatted
        except Exception as e:
            print(f"[Agent 1] Error loading mock data: {e}")
            return []

# ============================================================================
#  AGENT 1 — AdvancedEventAgent
# ============================================================================
class AdvancedEventAgent:
    """
    Agent 1: Event Detection & Classification
    -----------------------------------------
    - FinBERT  -> sentiment score  (-1.0 ... +1.0)
    - spaCy    -> named entity extraction (ORG, GPE)
    - Gemini   -> event_type, category, directional_bias, confidence
    """

    def __init__(self):
        self.mock_mode = MOCK_MODE
        print("[Agent 1] Initializing Event Detection Agent (Gemini)...")

        if not self.mock_mode:
            self.client = genai.Client(api_key=GEMINI_API_KEY)

            # FinBERT
            print(f"[Agent 1] Loading {FINBERT_MODEL}...")
            self.sentiment_analyzer = hf_pipeline(
                "sentiment-analysis", model=FINBERT_MODEL
            )

            # spaCy
            print(f"[Agent 1] Loading {SPACY_MODEL}...")
            try:
                self.nlp = spacy.load(SPACY_MODEL)
            except OSError:
                print(f"  [WARN] {SPACY_MODEL} not found. Run: python -m spacy download {SPACY_MODEL}")
                self.nlp = None

    # ── Local NLP helpers ───────────────────────────────────────────────────
    def _get_finbert_sentiment(self, text: str) -> float:
        if self.mock_mode:
            return 0.5
        result = self.sentiment_analyzer(text)[0]
        label, score = result["label"], result["score"]
        if label == "positive":
            return score
        elif label == "negative":
            return -score
        return 0.0

    def _get_spacy_entities(self, text: str) -> list:
        if self.mock_mode or not self.nlp:
            return ["OPEC"]
        doc = self.nlp(text)
        seen, entities = set(), []
        for ent in doc.ents:
            if ent.label_ in ("ORG", "GPE") and ent.text not in seen:
                entities.append(ent.text)
                seen.add(ent.text)
        return entities

    # ── Main processing ─────────────────────────────────────────────────────
    def process_news(self, news_text: str, timestamp: str, source: str = "Unknown") -> EventOutput:
        event_id = f"EVT_{uuid.uuid4().hex[:8].upper()}"
        processing_time = datetime.now(timezone.utc).isoformat()

        sentiment_score = self._get_finbert_sentiment(news_text)
        entities = self._get_spacy_entities(news_text)

        # ── Mock path ───────────────────────────────────────────────────────
        if self.mock_mode:
            return EventOutput(
                event_id=event_id, timestamp=timestamp, headline=news_text,
                event_type="Supply Shock", category="Energy Policy",
                entities=entities, directional_bias="Bullish Brent",
                confidence_score=0.91, source=source,
                sentiment_score=sentiment_score, raw_text=news_text,
                processing_timestamp=processing_time,
            )

        # ── Live Gemini path ────────────────────────────────────────────────
        system_prompt = f"""
        You are an elite financial event extraction agent specializing in global oil markets (Brent Crude).
        Your task is to classify the provided news text, considering the pre-calculated sentiment and entities.

        Pre-calculated Context:
        - Sentiment Score: {sentiment_score:.2f} (-1.0 is extremely negative, +1.0 extremely positive)
        - Extracted Entities: {', '.join(entities) if entities else 'None detected'}

        Output MUST be a valid JSON object:
        {{
            "event_type": "string (e.g., Supply Shock, Demand Shift, Geopolitical Tension)",
            "category": "string (e.g., Energy Policy, Macroeconomics)",
            "directional_bias": "string (Bullish Brent, Bearish Brent, Neutral)",
            "confidence_score": "float between 0.0 and 1.0"
        }}
        """

        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=f"News Headline: {news_text}",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                ),
            )
            result_dict = json.loads(response.text)
            return EventOutput(
                event_id=event_id, timestamp=timestamp, headline=news_text,
                event_type=result_dict.get("event_type", "Unknown"),
                category=result_dict.get("category", "Unknown"),
                entities=entities,
                directional_bias=result_dict.get("directional_bias", "Neutral"),
                confidence_score=result_dict.get("confidence_score", 0.5),
                source=source, sentiment_score=sentiment_score,
                raw_text=news_text, processing_timestamp=processing_time,
            )
        except Exception as e:
            print(f"  [WARN] Gemini API error: {e}. Falling back to rule-based.")
            return EventOutput(
                event_id=event_id, timestamp=timestamp, headline=news_text,
                event_type="Unknown Error", category="Unknown",
                entities=entities, directional_bias="Neutral",
                confidence_score=0.1, source=source,
                sentiment_score=sentiment_score, raw_text=news_text,
                processing_timestamp=processing_time,
            )

# ============================================================================
#  MAIN — Run Agent 1
# ============================================================================
def main():
    print("=" * 70)
    print("  AGENT 1 -- EVENT DETECTION & CLASSIFICATION")
    print("=" * 70)

    # 1. Load data
    scraper = MockNewsScraper()
    news_data = scraper.fetch_news()

    # 2. Initialize agent
    agent = AdvancedEventAgent()

    # 3. Process each article
    events = []
    total = len(news_data)
    for i, article in enumerate(news_data):
        print(f"\n[{i+1}/{total}] Processing: {article['headline'][:80]}...")
        event = agent.process_news(
            news_text=article["headline"],
            timestamp=article["timestamp"],
            source=article["source"],
        )
        events.append(event)
        print(f"  -> Event Type : {event.event_type}")
        print(f"  -> Sentiment  : {event.sentiment_score:.2f}")
        print(f"  -> Bias       : {event.directional_bias}")
        print(f"  -> Confidence : {event.confidence_score:.2f}")

        # Rate limit (skip on last article)
        if not MOCK_MODE and i < total - 1:
            time.sleep(RATE_LIMIT_SEC)

    # 4. Save output
    os.makedirs("data/processed", exist_ok=True)
    output_path = "data/processed/a1_events.json"
    with open(output_path, "w") as f:
        json.dump([e.model_dump() for e in events], f, indent=4)
    print(f"\n[OK] Agent 1 complete -- saved {len(events)} events to {output_path}")
    print("   -> Next step: python agent2_macro_debate.py")

if __name__ == "__main__":
    main()
