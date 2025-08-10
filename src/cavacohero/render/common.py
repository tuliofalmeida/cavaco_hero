# src/cavacohero/render/common.py
from typing import Iterable, Tuple
import matplotlib.pyplot as plt

def auto_window(frets: Iterable, pad: int = 1, min_span: int = 4) -> Tuple[int, int]:
    """Pick [start,end] frets for a tight zoom. Ignores zeros when possible."""
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

def setup_axes_vertical(strings: int, y0: float, y1: float, ax=None, figsize=(4, 12)):
    """Create/clear a vertical fretboard axes: strings = x (0..strings-1), frets = y (0..N)."""
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, dpi=120)
    else:
        fig = ax.figure
        ax.clear()
    ax.set_xlim(-0.75, strings - 0.25)
    ax.set_ylim(y0, y1)
    ax.invert_yaxis()      # nut at the top
    ax.axis("off")
    return fig, ax

def draw_grid_vertical(ax, strings: int, y0: int, y1: int):
    """Black strings + frets; thick nut at 0 if in range."""
    # strings (vertical)
    for s in range(strings):
        ax.plot([s, s], [y0, y1], color="black", linewidth=2)
    # frets (horizontal)
    start, end = int(y0), int(y1)
    for f in range(start, end + 1):
        lw = 3 if f == 0 else 1
        ax.plot([-0.5, strings - 0.5], [f, f], color="black", linewidth=lw)

def label_vertical(ax, tuning, y0: float, y1: float):
    # tuning above nut
    for s, note in enumerate(tuning):
        ax.text(s, y0 - 0.4, note, ha="center", va="bottom", fontsize=10)
    # fret numbers on the left
    for f in range(int(y0), int(y1) + 1):
        ax.text(-0.65, f, str(f), va="center", ha="right", fontsize=8)

def plot_notes_vertical(ax, frets, strings: int, y0: float, y1: float, color="red", show_mutes=True):
    """Red dots between frets. No 'O' markers. Optional 'X' for mutes."""
    for s_idx, fret in enumerate(frets):
        if isinstance(fret, int):
            if 1 <= fret <= y1:
                ax.scatter(s_idx, fret - 0.5, s=140, zorder=3, color=color)
        elif show_mutes and isinstance(fret, str) and fret.lower() == "x":
            ax.text(s_idx, y0 - 0.25, "X", ha="center", va="bottom", fontsize=10)
