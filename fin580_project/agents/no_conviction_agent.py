from agents.signal_agent import SignalAgent

class NoConvictionAgent(SignalAgent):
    def generate_signal(self, event):
        result = super().generate_signal(event)

        result["conviction"] = 3  # fixed

        return result