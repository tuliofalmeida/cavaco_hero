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


def parse_cavaco_shape(name: str, encoded: Sequence[Union[int, str]], strings_expected: int = 4) -> TabShape:
    """
    Parse a cavaco-encoded shape list into a TabShape.

    Encoding rules:
      - Each item is either:
          * an int like 42 (string=4, fret=2), 30 (string=3, fret=0), or
          * a string "x" / "X" to mute that string.
      - Order must be string 4, 3, 2, 1 (descending).
      - Fret can be multi-digit (e.g., 410 -> string=4, fret=10).

    Example:
      name="C", encoded=[42, 30, 21, 12] -> TabShape("C", (2, 0, 1, 2))
    """
    if len(encoded) != strings_expected:
        raise ValueError(f"{name}: expected {strings_expected} items (strings 4→1), got {len(encoded)}")

    result: list[Fret] = []
    # expected order: 4,3,2,1 (or strings_expected down to 1)
    expected_strings = list(range(strings_expected, 0, -1))

    for idx, token in enumerate(encoded):
        expected_string = expected_strings[idx]

        # handle mute
        if isinstance(token, str):
            if token.lower() != "x":
                raise ValueError(f"{name}: token '{token}' invalid (use int or 'x')")
            result.append("x")
            continue

        # convert int token to text so we can handle multi-digit frets
        if isinstance(token, int):
            text = str(token)
        else:
            # defensive: allow numeric strings like "42"
            text = str(token)

        if not text.isdigit():
            raise ValueError(f"{name}: token '{token}' is not numeric or 'x'")

        # first char = string number; remaining chars = fret (can be >9)
        string_num = int(text[0])
        fret_part = text[1:] or "0"  # if someone writes "4" treat as fret 0
        try:
            fret_num = int(fret_part)
        except ValueError:
            raise ValueError(f"{name}: bad fret in token '{token}'")

        if string_num != expected_string:
            raise ValueError(
                f"{name}: token '{token}' says string {string_num} but position {idx} expects string {expected_string} "
                f"(order must be {strings_expected}→…→1)."
            )
        if fret_num < 0:
            raise ValueError(f"{name}: negative fret {fret_num} in token '{token}'")

        result.append(fret_num)

    shape = TabShape(name=name, frets=tuple(result))
    shape.validate(strings_expected)
    return shape
