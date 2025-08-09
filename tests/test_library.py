from pathlib import Path
from cavacohero.theory.library import load_library

def test_load_cavaco_yaml():
    path = Path(__file__).resolve().parents[1] / "presets" / "chords.yaml"
    tuning, shapes = load_library(path)
    assert tuning == ("D","G","B","D")
    assert "C" in shapes
    c0 = shapes["C"][0]
    assert c0.frets == (2,0,1,2)  # from [42,30,21,12]

def test_multi_digit_frets():
    from cavacohero.theory.tabs import parse_cavaco_shape
    shape = parse_cavaco_shape("Fake", [45, 34, 212, 112], strings_expected=4)
    assert shape.frets == (5, 4, 12, 12)