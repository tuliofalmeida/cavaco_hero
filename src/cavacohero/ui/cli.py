# src/cavacohero/ui/cli.py
import time
from pathlib import Path
import matplotlib.pyplot as plt

from ..theory.library import load_library

# optional: advanced selector (if you created it)
try:
    from ..theory.select import select_chords as _select
except Exception:
    _select = None

# draw functions
from ..render.fretboard import draw_shape as draw_zoom
from ..render.fretboard_full import draw_shape_full

def run_cli():
    data = load_library(Path("presets/chords.yaml"))

    # Support both loader signatures:
    #   old: (tuning, shapes)
    #   new: (tuning, shapes_by_name, meta_by_name, sets)
    if isinstance(data, tuple) and len(data) == 4:
        tuning, shapes_by_name, meta_by_name, sets = data
    elif isinstance(data, tuple) and len(data) == 2:
        tuning, shapes_by_name = data
        meta_by_name = {k: {} for k in shapes_by_name}
        sets = {"all": {"include": "*"}}
    else:
        raise RuntimeError("Unexpected load_library() return format.")

    def pick_names(selection="all", custom_list=None):
        # If you have the formal selector, use it
        if _select:
            if selection == "custom" and custom_list:
                return [n for n in custom_list if n in shapes_by_name]
            return _select(shapes_by_name, meta_by_name, sets, selection)

        # Fallback (simple heuristics if you haven't added the selector yet)
        names = sorted(shapes_by_name.keys())
        if selection == "major":
            return [n for n in names if not n.endswith("m")]
        if selection == "minor":
            return [n for n in names if n.endswith("m")]
        # (you can add more heuristics here)
        return names

    mode = "zoom"      # "zoom" | "full"
    names = pick_names("all")
    if not names:
        print("No chords matched your selection.")
        return

    i = 0

    # Start with a zoom window
    fig, ax = plt.subplots(figsize=(3.2, 5.0), dpi=120)
    draw_zoom(shapes_by_name[names[i]][0], ax=ax)
    plt.show(block=False); plt.pause(0.01)

    print("Commands: n p q | mode zoom|full | set all|major|minor|sevenths|my_progression|custom")

    while True:
        cmd = input("> ").strip().lower()

        if cmd == "q":
            break

        elif cmd == "n":
            i = (i + 1) % len(names)

        elif cmd == "p":
            i = (i - 1) % len(names)

        elif cmd.startswith("mode"):
            _, _, token = cmd.partition(" ")
            if token in ("zoom", "full"):
                mode = token
                # Create a fresh window for each mode to keep sizing simple/predictable
                plt.close('all')
                if mode == "zoom":
                    fig, ax = plt.subplots(figsize=(3.2, 5.0), dpi=120)
                print(f"view: {mode}")
            else:
                print("Use: mode zoom|full")
                continue

        elif cmd.startswith("set"):
            _, _, token = cmd.partition(" ")
            if token == "custom":
                raw = input("Enter chords comma-separated: ")
                custom = [s.strip() for s in raw.split(",") if s.strip()]
                names = pick_names("custom", custom_list=custom)
            else:
                names = pick_names(token or "all")
            i = 0
            print(f"set: {token or 'all'} ({len(names)} chords)")
            if not names:
                print("No chords matched that set.")
                continue
            
        elif cmd.startswith("auto"):
            parts = cmd.split()
            delay = 3.0
            randomize = False

            for p in parts[1:]:
                if p.replace('.', '', 1).isdigit():
                    delay = float(p)
                elif p in ("random", "rand", "shuffle"):
                    randomize = True

            autoplay(names, shapes_by_name, mode=mode, delay=delay, randomize=randomize)
            continue

        else:
            print("Commands: n p q | mode zoom|full | set all|major|minor|sevenths|my_progression|custom")
            continue

        # Draw current chord in current mode
        if mode == "zoom":
            draw_zoom(shapes_by_name[names[i]][0], ax=ax)
            plt.pause(0.01)
        else:
            # Full-neck always opens a tall figure so height changes actually stick
            draw_shape_full(shapes_by_name[names[i]][0], height_in=14.0)
            plt.show(block=False); plt.pause(0.01)


import time
import random

def autoplay(names, shapes_by_name, mode="zoom", delay=3.0, randomize=False):
    """
    Loop through given chord names, displaying each for 'delay' seconds
    in fullscreen until interrupted (Ctrl+C).
    If randomize=True, shuffle the order each time.
    """
    plt.ion()
    try:
        while True:
            chord_order = names.copy()
            if randomize:
                random.shuffle(chord_order)

            for chord_name in chord_order:
                if mode == "zoom":
                    fig, ax = plt.subplots(figsize=(3.2, 5.0), dpi=120)
                    draw_zoom(shapes_by_name[chord_name][0], ax=ax)
                else:
                    fig, ax = draw_shape_full(shapes_by_name[chord_name][0], height_in=14.0)

                plt.pause(0.01)
                time.sleep(delay)
                plt.close(fig)
    except KeyboardInterrupt:
        print("\nAutoplay stopped.")
    finally:
        plt.ioff()

