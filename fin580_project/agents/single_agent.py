import random

class SingleAgent:
    def generate_signal(self, event):
        # simple heuristic (no multi-step reasoning)

        if "supply" in event.get("macro_thesis", "").lower():
            signal = "LONG"
        elif "demand" in event.get("macro_thesis", "").lower():
            signal = "SHORT"
        else:
            signal = random.choice(["LONG", "SHORT", "FLAT"])

        return {
            "timestamp": event["timestamp"],
            "event_type": event["event_type"],
            "signal": signal,
            "conviction": 3,
            "horizon": "medium"
        }