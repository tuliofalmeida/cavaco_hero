from __future__ import annotations
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Any
from .tabs import TabShape, parse_cavaco_shape

DEFAULT_TUNING = ("D", "G", "B", "D")

def load_library(p: Path) -> tuple[tuple[str, ...], Dict[str, List[TabShape]], Dict[str, dict], dict]:
    """
    Loads the new YAML schema:
      tuning: [...]
      chords:
        NAME:
          quality: ...
          tags: [...]
          shapes: [[42,30,21,12], ...]
      sets:
        ...
    Returns: (tuning, shapes_by_name, meta_by_name, sets)
    """
    data = yaml.safe_load(p.read_text(encoding="utf-8"))

    tuning = tuple(data.get("tuning", DEFAULT_TUNING))
    strings_expected = len(tuning)

    shapes_by_name: Dict[str, List[TabShape]] = {}
    meta_by_name: Dict[str, dict] = {}

    chords = data.get("chords", {})
    if not isinstance(chords, dict):
        raise ValueError("'chords' must be a mapping")

    for name, spec in chords.items():
        if not isinstance(spec, dict):
            raise ValueError(f"Chord '{name}' must be a mapping with quality/tags/shapes")
        variants = spec.get("shapes", [])
        if not isinstance(variants, list) or not variants:
            raise ValueError(f"Chord '{name}' must have a non-empty 'shapes' list")

        parsed: List[TabShape] = []
        for raw in variants:
            if not isinstance(raw, (list, tuple)):
                raise ValueError(f"Chord '{name}' shape must be a list like [42,30,21,12]")
            parsed.append(parse_cavaco_shape(name, raw, strings_expected=strings_expected))

        shapes_by_name[name] = parsed
        meta_by_name[name] = {
            "quality": spec.get("quality"),
            "tags": set(spec.get("tags", [])),
        }

    sets = data.get("sets", {})
    if sets is None: sets = {}
    if not isinstance(sets, dict):
        raise ValueError("'sets' must be a mapping if present")

    return tuning, shapes_by_name, meta_by_name, sets
