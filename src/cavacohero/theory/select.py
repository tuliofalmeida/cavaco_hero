from __future__ import annotations
from typing import Dict, List, Iterable
from .tabs import TabShape

def select_chords(
    shapes_by_name: Dict[str, List[TabShape]],
    meta_by_name: Dict[str, dict],
    sets: dict,
    selection: str | Iterable[str] = "all",
) -> List[str]:
    names = list(shapes_by_name.keys())

    # explicit list from user: ["C","Dm","G7"]
    if isinstance(selection, (list, tuple)):
        return [n for n in selection if n in shapes_by_name]

    # named set in YAML
    if isinstance(selection, str) and selection in sets:
        rule = sets[selection] or {}
        include = rule.get("include")
        quals  = set(rule.get("qualities", []))
        tags   = set(rule.get("tags", []))

        picked = set()
        if include == "*" or selection == "all":
            picked.update(names)
        elif isinstance(include, list):
            picked.update([n for n in include if n in shapes_by_name])

        if quals:
            picked.update([n for n,m in meta_by_name.items() if m.get("quality") in quals])
        if tags:
            picked.update([n for n,m in meta_by_name.items() if m.get("tags") & tags])

        return sorted(picked)

    # convenience shortcuts
    if selection == "all":
        return sorted(names)
    if selection == "major":
        return sorted([n for n,m in meta_by_name.items() if m.get("quality") == "major"])
    if selection == "minor":
        return sorted([n for n,m in meta_by_name.items() if m.get("quality") == "minor"])

    # unknown token → fallback to empty (or all, your call)
    return []
