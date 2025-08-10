# src/cavacohero/render/fretboard_full.py
import matplotlib.pyplot as plt
from typing import Tuple
from ..theory.tabs import TabShape
from ..instrument.cavaco import CAVACO

DEFAULT_TUNING = CAVACO.tuning

def draw_shape_full(
    tab_shape: TabShape,
    tuning: Tuple[str, ...] = DEFAULT_TUNING,
    max_fret: int | None = None,
    height_in: float = 10.0,   # <— control the Y size here
):
    """
    Full-neck vertical chord diagram. Always creates a NEW figure
    so 'height_in' is respected regardless of the caller.
    """
    strings = len(tuning)
    max_fret = max_fret or getattr(CAVACO, "max_fret", 15)

    # NEW figure with the exact height requested
    fig, ax = plt.subplots(figsize=(3.2, height_in), dpi=85)

    # coord: x=string, y=fret
    ax.set_xlim(-0.75, strings - 0.25)
    ax.set_ylim(-0.5, max_fret + 0.5)
    ax.invert_yaxis()
    ax.axis("off")

    # strings (vertical) + frets (horizontal)
    for s in range(strings):
        ax.plot([s, s], [0, max_fret], color="black", linewidth=2)
    for f in range(max_fret + 1):
        lw = 3 if f == 0 else 1
        ax.plot([-0.5, strings - 0.5], [f, f], color="black", linewidth=lw)

    # labels
    for s, note in enumerate(tuning):
        ax.text(s, -0.4, note, ha="center", va="bottom", fontsize=10)
    for f in range(max_fret + 1):
        ax.text(-0.65, f, str(f), va="center", ha="right", fontsize=8)

    # red dots (between frets), no open "O"
    for s_idx, fret in enumerate(tab_shape.frets):
        if isinstance(fret, int) and 1 <= fret <= max_fret:
            ax.scatter(s_idx, fret - 0.5, s=140, zorder=3, color="red")
        elif isinstance(fret, str) and fret.lower() == "x":
            ax.text(s_idx, -0.25, "X", ha="center", va="bottom", fontsize=10)

    ax.set_title(f"{tab_shape.name}", fontsize=12, pad=16)
    fig.tight_layout()
    return fig, ax
