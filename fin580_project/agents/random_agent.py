import random

class RandomAgent:
    def generate_signal(self, event):
        signal = random.choice(["LONG", "SHORT", "FLAT"])

        return {
            "timestamp": event["timestamp"],
            "event_type": event["event_type"],
            "signal": signal,
            "conviction": 3,
            "horizon": "medium"
        }