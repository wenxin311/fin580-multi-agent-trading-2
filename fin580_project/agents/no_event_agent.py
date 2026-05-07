class NoEventAgent:
    def generate_signal(self, event):
        return {
            "timestamp": event["timestamp"],
            "event_type": event["event_type"],
            "signal": "LONG",   # naive
            "conviction": 3,
            "horizon": "medium"
        }