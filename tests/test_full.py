from pathlib import Path
from cavacohero.theory.library import load_library
from cavacohero.render.fretboard_full import draw_shape_full
import matplotlib.pyplot as plt

def test_draw_shape_full():
    """Manual visual test for full-neck vertical plot."""
    tuning, shapes = load_library(Path("presets/chords.yaml"))
    fig, _ = draw_shape_full(shapes["C"][0])
    plt.show()

if __name__ == "__main__":
    test_draw_shape_full()