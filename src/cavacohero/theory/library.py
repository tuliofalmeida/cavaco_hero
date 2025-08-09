# src/cavacohero/theory/library.py
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

from .tabs import TabShape, parse_cavaco_shape

DEFAULT_TUNING = ("D", "G", "B", "D")  # cavaco default

def load_library(chords_yaml: Path) -> Tuple[Tuple[str, ...], Dict[str, List[TabShape]]]:
    """
    Load chords from YAML using cavaco encoding.
    Returns (tuning, shapes_by_name).

    YAML format:
      tuning: ["D","G","B","D"]
      chords:
        C:
          - [42, 30, 21, 12]
        D:
          - [44, 32, 23, 14]
        ...

    The list for each chord must be ordered strings 4→3→2→1.
    """
    data = yaml.safe_load(chords_yaml.read_text(encoding="utf-8"))
    tuning = tuple(data.get("tuning", DEFAULT_TUNING))
    strings_expected = len(tuning)

    shapes_by_name: Dict[str, List[TabShape]] = {}

    chords = data.get("chords", {})
    if not isinstance(chords, dict):
        raise ValueError("YAML 'chords' must be a mapping from name to list of shapes")

    for name, variants in chords.items():
        if not isinstance(variants, list):
            raise ValueError(f"Chord '{name}' must map to a list of shapes")
        parsed_variants: List[TabShape] = []
        for raw_shape in variants:
            if not isinstance(raw_shape, (list, tuple)):
                raise ValueError(f"Chord '{name}' variant must be a list like [42, 30, 21, 12]")
            shape = parse_cavaco_shape(name, raw_shape, strings_expected=strings_expected)
            parsed_variants.append(shape)
        shapes_by_name[name] = parsed_variants

    return tuning, shapes_by_name
