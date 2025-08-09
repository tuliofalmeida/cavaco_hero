# src/cavacohero/ui/cli.py
from pathlib import Path
import time
import matplotlib.pyplot as plt

from ..theory.library import load_library
from ..render.fretboard import draw_shape

def run_cli():
    repo_root = Path(__file__).resolve().parents[3]  # three levels up
    chords_yaml = repo_root / "presets" / "chords.yaml"
    tuning, shapes = load_library(chords_yaml)
    names = sorted(shapes.keys())
    i = 0
    timer_enabled = False
    tempo_s = 3.0
    next_tick = time.monotonic() + tempo_s

    print("CavacoHero — n: next, p: prev, r: random, t: toggle timer, q: quit")

    fig, ax = plt.subplots(figsize=(3.2,5.0), dpi=120)
    draw_shape(shapes[names[i]][0], ax=ax)
    plt.show(block=False)

    while True:
        # timer tick
        now = time.monotonic()
        if timer_enabled and now >= next_tick:
            i = (i + 1) % len(names)
            fig = draw_shape(shapes[names[i]][0])
            plt.show(block=False)
            plt.pause(0.01)
            next_tick = now + tempo_s

        try:
            cmd = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        if cmd == "q":
            break
        elif cmd == "n":
            i = (i + 1) % len(names)
        elif cmd == "p":
            i = (i - 1) % len(names)
        elif cmd == "r":
            import random
            i = random.randrange(len(names))
        elif cmd == "t":
            timer_enabled = not timer_enabled
            print(f"timer_enabled = {timer_enabled}")
            next_tick = time.monotonic() + tempo_s
        else:
            print("commands: n p r t q")
            continue

        draw_shape(shapes[names[i]][0], ax=ax)
        # plt.show(block=False)
        plt.pause(0.01)
