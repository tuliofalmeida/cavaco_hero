import matplotlib.pyplot as plt
from typing import Iterable, Tuple
from ..theory.tabs import TabShape

DEFAULT_TUNING = ("D", "G", "B", "D")

def _auto_window(frets: Iterable, pad: int = 1, min_span: int = 4) -> Tuple[int, int]:
    nums = [f for f in frets if isinstance(f, int) and f >= 0]
    if not nums:
        return 0, max(min_span, 4)
    mn = min([f for f in nums if f > 0] or [0])
    mx = max(nums)
    if mx <= 3:
        return 0, max(3, min_span)
    start = max(1, mn - pad)
    end = max(start + min_span, mx + pad)
    return start, end

def draw_shape(
    tab_shape: TabShape,
    tuning: Tuple[str, ...] = DEFAULT_TUNING,
    ax=None,
):
    strings = len(tuning)
    frets = tab_shape.frets

    start_fret, end_fret = _auto_window(frets)
    span = end_fret - start_fret

    if ax is None:
        fig, ax = plt.subplots(figsize=(3.2, 5.0), dpi=120)
    else:
        fig = ax.figure
        ax.clear()

    # set up axes
    ax.set_xlim(-0.75, strings - 0.25)
    ax.set_ylim(start_fret - 0.8, end_fret + 0.8)
    ax.invert_yaxis()
    ax.axis("off")

    # strings (black)
    for s in range(strings):
        ax.plot([s, s], [start_fret, end_fret], color="black", linewidth=2)

    # frets (black)
    for f in range(start_fret, end_fret + 1):
        lw = 3 if f == 0 else 1
        ax.plot([-0.5, strings - 0.5], [f, f], color="black", linewidth=lw)

    # tuning labels
    for s in range(strings):
        ax.text(s, start_fret - 0.45, tuning[s], ha="center", va="bottom", fontsize=10)

    # fret numbers
    for f in range(start_fret, end_fret + 1):
        ax.text(-0.65, f, str(f), va="center", ha="right", fontsize=8)

    # note dots (red)
    for s_idx, fret in enumerate(frets):
        if isinstance(fret, int):
            if fret > 0 and start_fret <= fret <= end_fret:
                ax.scatter(
                    s_idx,
                    fret - 0.5,    # shift to between frets
                    s=220,
                    zorder=3,
                    color="red"
                )
        elif isinstance(fret, str) and fret.lower() == "x":
            ax.text(s_idx, start_fret - 0.25, "X", ha="center", va="bottom", fontsize=10)

    ax.set_title(tab_shape.name, fontsize=12, pad=6)
    fig.tight_layout()
    return fig, ax
