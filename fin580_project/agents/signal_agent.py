import json

class SignalAgent:
    def __init__(self):
        pass

    def generate_signal(self, event):
        thesis = event["macro_thesis"].lower()

        # 簡單 rule-based（之後可以換成 LLM）
        if "increase" in thesis or "higher" in thesis:
            signal = "LONG"
            conviction = 5
            horizon = "medium"

        elif "decrease" in thesis or "slowdown" in thesis:
            signal = "SHORT"
            conviction = 3
            horizon = "medium"

        else:
            signal = "FLAT"
            conviction = 2
            horizon = "short"

        return {
            "timestamp": event["timestamp"],
             "event_type": event["event_type"],
            "signal": signal,
            "conviction": conviction,
            "horizon": horizon
        }