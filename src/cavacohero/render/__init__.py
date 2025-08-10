from .fretboard import draw_shape as draw_zoom
from .fretboard_full import draw_shape_full as draw_full

def draw(tab_shape, mode="zoom", **kwargs):
    """Draw a chord shape in zoom or full-neck mode."""
    if mode == "full":
        return draw_full(tab_shape, **kwargs)
    return draw_zoom(tab_shape, **kwargs)
