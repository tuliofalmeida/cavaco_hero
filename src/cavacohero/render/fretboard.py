# src/cavacohero/render/fretboard.py
from typing import Tuple
from ..theory.tabs import TabShape
from ..instrument.cavaco import CAVACO
from .common import auto_window, setup_axes_vertical, draw_grid_vertical, label_vertical, plot_notes_vertical

DEFAULT_TUNING = CAVACO.tuning

def draw_shape(tab_shape: TabShape, tuning: Tuple[str, ...] = DEFAULT_TUNING, ax=None):
    strings = len(tuning)
    y0, y1 = auto_window(tab_shape.frets)  # choose a tight window
    fig, ax = setup_axes_vertical(strings, y0 - 0.8, y1 + 0.8, ax=ax, figsize=(3.2, 5.0))
    draw_grid_vertical(ax, strings, y0, y1)
    label_vertical(ax, tuning, y0, y1)
    plot_notes_vertical(ax, tab_shape.frets, strings, y0, y1, color="red", show_mutes=True)
    ax.set_title(tab_shape.name, fontsize=12, pad=6)
    fig.tight_layout()
    return fig, ax
