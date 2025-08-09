from dataclasses import dataclass

@dataclass(frozen=True)
class Instrument:
    name: str
    strings: int
    tuning: tuple[str, ...]          # low->high, e.g. ("D","G","B","D")
    max_fret: int = 15

CAVACO = Instrument(
    name="cavaco",
    strings=4,
    tuning=("D","G","B","D"),        # cavaco tuning
    max_fret=15
)
