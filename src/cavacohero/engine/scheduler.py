import time

class Scheduler:
    def __init__(self, state):
        self.state = state
        self._next = time.monotonic()

    def tick_if_due(self):
        now = time.monotonic()
        if now >= self._next:
            self._next = now + self.state.tempo_s
            return True
        return False
