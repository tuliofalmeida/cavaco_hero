# src/cavacohero/theory/tabs.py
from dataclasses import dataclass
from typing import Union, Sequence

Fret = Union[int, str]  # int >= 0 or "x"

@dataclass(frozen=True)
class TabShape:
    name: str
    frets: tuple[Fret, ...]  # index 0 = string 4 (lowest), index 3 = string 1 (highest)

    def validate(self, strings_expected: int) -> None:
        if len(self.frets) != strings_expected:
            raise ValueError(f"{self.name}: expected {strings_expected} strings, got {len(self.frets)}")
        for f in self.frets:
            if isinstance(f, int):
                if f < 0:
                    raise ValueError(f"{self.name}: negative fret {f}")
            elif isinstance(f, str):
                if f.lower() != "x":
                    raise ValueError(f"{self.name}: bad symbol {f} (use int or 'x')")
            else:
                raise ValueError(f"{self.name}: invalid fret type {type(f)}")


# src/cavacohero/theory/tabs.py

def parse_cavaco_shape(name: str, encoded: Sequence[Union[int, str]], strings_expected: int = 4) -> TabShape:
    """
    Cavaco encoding: first digit = string (1..strings_expected), remaining digits = fret (0..∞).
    Supports multi-digit frets, e.g. 112 -> string 1, fret 12.
    Order in the list must be strings_expected → ... → 1 (e.g., 4,3,2,1 for cavaco).
    'x' or 'X' = mute.
    """
    if len(encoded) != strings_expected:
        raise ValueError(f"{name}: expected {strings_expected} items (strings {strings_expected}→…→1), got {len(encoded)}")

    result: list[Fret] = []
    expected_strings = list(range(strings_expected, 0, -1))

    for idx, token in enumerate(encoded):
        expected_string = expected_strings[idx]

        # mute
        if isinstance(token, str) and token.lower() == "x":
            result.append("x")
            continue

        # allow ints or numeric strings; convert to text
        text = str(token)
        if not text.isdigit():
            raise ValueError(f"{name}: token '{token}' must be an integer like 42 or 'x'")

        # first digit = string id, rest = fret (may be multi-digit, default 0)
        string_num = int(text[0])
        fret_part = text[1:] or "0"
        fret_num = int(fret_part)

        if not (1 <= string_num <= strings_expected):
            raise ValueError(f"{name}: string {string_num} out of range 1..{strings_expected} in token '{token}'")
        if string_num != expected_string:
            raise ValueError(f"{name}: token '{token}' says string {string_num} but position expects string {expected_string} "
                             f"(order must be {strings_expected}→…→1)")
        if fret_num < 0:
            raise ValueError(f"{name}: negative fret in token '{token}'")

        result.append(fret_num)

    shape = TabShape(name=name, frets=tuple(result))
    shape.validate(strings_expected)
    return shape

