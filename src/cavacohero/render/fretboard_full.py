# src/cavacohero/render/fretboard_full.py
import matplotlib.pyplot as plt
from typing import Tuple
from ..theory.tabs import TabShape
from ..instrument.cavaco import CAVACO  # has tuning and max_fret

DEFAULT_TUNING = CAVACO.tuning

def draw_shape_full(
    tab_shape: TabShape,
    tuning: Tuple[str, ...] = DEFAULT_TUNING,
    ax=None,
    max_fret: int | None = None,
):
    """
    Full-neck vertical chord diagram:
      - strings vertical (left=4 .. right=1)
      - frets horizontal from 0..max_fret
      - note dots red, lines black, dots between frets
      - no 'O' open markers
    """
    strings = len(tuning)
    max_fret = max_fret or getattr(CAVACO, "max_fret", 15)

    # create figure/axes
    if ax is None:
        fig, ax = plt.subplots(figsize=(3.2, 8.0), dpi=120)
    else:
        fig = ax.figure
        ax.clear()

    # limits: x=string, y=fret
    ax.set_xlim(-0.75, strings - 0.25)
    ax.set_ylim(-0.5, max_fret + 0.5)
    ax.invert_yaxis()  # fret 0 (nut) at top
    ax.axis("off")

    # draw strings (vertical, black)
    for s in range(strings):
        ax.plot([s, s], [0, max_fret], color="black", linewidth=2)

    # draw frets (horizontal, black) — nut thicker
    for f in range(max_fret + 1):
        lw = 3 if f == 0 else 1
        ax.plot([-0.5, strings - 0.5], [f, f], color="black", linewidth=lw)

    # tuning labels (above nut)
    for s in range(strings):
        ax.text(s, -0.4, tuning[s], ha="center", va="bottom", fontsize=10)

    # fret numbers (left side)
    for f in range(max_fret + 1):
        ax.text(-0.65, f, str(f), va="center", ha="right", fontsize=8)

    # dots for notes (between frets)
    for s_idx, fret in enumerate(tab_shape.frets):
        if isinstance(fret, int):
            if fret > 0 and fret <= max_fret:
                ax.scatter(s_idx, fret - 0.5, s=140, zorder=3, color="red")
        elif isinstance(fret, str) and fret.lower() == "x":
            ax.text(s_idx, -0.25, "X", ha="center", va="bottom", fontsize=10)

    ax.set_title(f"{tab_shape.name}", fontsize=12, pad=16)
    fig.tight_layout()
    return fig, ax