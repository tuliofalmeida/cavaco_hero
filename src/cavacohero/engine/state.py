import random
from ..theory.chords import ALL_CHORDS

class AppState:
    def __init__(self, tempo_s=3.0, timer_enabled=False):
        self.tempo_s = tempo_s
        self.timer_enabled = timer_enabled
        self._i = 0
        self._order = list(range(len(ALL_CHORDS)))

    def current_chord(self):
        return ALL_CHORDS[self._order[self._i]]

    def next_chord(self):
        self._i = (self._i + 1) % len(self._order)

    def prev_chord(self):
        self._i = (self._i - 1) % len(self._order)

    def random_chord(self):
        self._i = random.randrange(len(self._order))
