from pathlib import Path
from cavacohero.theory.library import load_library

def test_load_cavaco_yaml():
    path = Path(__file__).resolve().parents[1] / "presets" / "chords.yaml"
    tuning, shapes = load_library(path)
    assert tuning == ("D","G","B","D")
    assert "C" in shapes
    c0 = shapes["C"][0]
    assert c0.frets == (2,0,1,2)  # from [42,30,21,12]
