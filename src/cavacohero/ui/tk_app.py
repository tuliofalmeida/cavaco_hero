import tkinter as tk
from tkinter import ttk, messagebox

import random
from pathlib import Path

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from ..theory.library import load_library

# optional selector (if you created it); otherwise we fall back to simple rules
try:
    from ..theory.select import select_chords as _select
except Exception:
    _select = None

# renderers
from ..render.fretboard import draw_shape as draw_zoom
from ..render.fretboard_full import draw_shape_full


class CavacoHeroTk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CavacoHero")
        self.geometry("1280x860")

        # ---- data ----
        data = load_library(Path("presets/chords.yaml"))
        if len(data) == 4:
            self.tuning, self.shapes_by_name, self.meta_by_name, self.sets = data
        else:
            self.tuning, self.shapes_by_name = data
            self.meta_by_name = {k: {} for k in self.shapes_by_name}
            self.sets = {"all": {"include": "*"}}

        # state
        self.mode = tk.StringVar(value="zoom")        # zoom | full
        self.current_set = tk.StringVar(value="all")  # all | major | minor | ...
        self.randomize = tk.BooleanVar(value=False)
        self.period_s = tk.DoubleVar(value=3.0)
        self.custom_list = tk.StringVar(value="")     # e.g., "C, Dm, G7"

        self.names = self._pick_names("all")
        self.idx = 0
        self._autoplay_job = None

        # ---- UI ----
        self._build_controls()
        self._build_canvas()

        self._render()  # first draw

    # ---------- UI BUILDERS ----------
    def _build_controls(self):
        bar = ttk.Frame(self)
        bar.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        ttk.Label(bar, text="Set:").pack(side=tk.LEFT, padx=(0,4))
        set_opts = sorted(list(self.sets.keys()) + ["major","minor","sevenths","custom","all"])
        self.set_combo = ttk.Combobox(bar, values=set_opts, textvariable=self.current_set, width=14, state="readonly")
        self.set_combo.pack(side=tk.LEFT)
        self.set_combo.bind("<<ComboboxSelected>>", self._on_set_change)

        ttk.Label(bar, text="Mode:").pack(side=tk.LEFT, padx=(12,4))
        mode_combo = ttk.Combobox(bar, values=["zoom","full"], textvariable=self.mode, width=8, state="readonly")
        mode_combo.pack(side=tk.LEFT)
        mode_combo.bind("<<ComboboxSelected>>", lambda e: self._render())

        ttk.Label(bar, text="Custom:").pack(side=tk.LEFT, padx=(12,4))
        custom_entry = ttk.Entry(bar, textvariable=self.custom_list, width=24)
        custom_entry.pack(side=tk.LEFT)
        ttk.Button(bar, text="Apply", command=self._apply_custom).pack(side=tk.LEFT, padx=(4,0))

        ttk.Separator(bar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        ttk.Button(bar, text="◀ Prev", command=self.prev).pack(side=tk.LEFT)
        ttk.Button(bar, text="Next ▶", command=self.next).pack(side=tk.LEFT, padx=(4,0))

        ttk.Separator(bar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        ttk.Label(bar, text="Period (s):").pack(side=tk.LEFT, padx=(0,4))
        period = ttk.Spinbox(bar, from_=0.2, to=60.0, increment=0.2, width=6, textvariable=self.period_s)
        period.pack(side=tk.LEFT)

        rnd = ttk.Checkbutton(bar, text="Random", variable=self.randomize)
        rnd.pack(side=tk.LEFT, padx=(10,0))

        self.start_btn = ttk.Button(bar, text="Start", command=self.start_autoplay)
        self.start_btn.pack(side=tk.LEFT, padx=(10,2))
        self.stop_btn = ttk.Button(bar, text="Stop", command=self.stop_autoplay, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT)

        # status
        self.status = ttk.Label(self, anchor="w", relief=tk.SUNKEN)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def _build_canvas(self):
        # Create one persistent Figure/Axes so the plot doesn't jump around
        self.fig = plt.Figure(figsize=(5.0, 6.0), dpi=120)   # fixed size inside the window
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

    # ---------- RENDER ----------
    def _render(self):
        if not self.names:
            self.ax.clear()
            self.ax.set_title("No chords in selection")
            self.canvas.draw()
            return

        chord_name = self.names[self.idx]
        shape = self.shapes_by_name[chord_name][0]

        # Clear the existing axes and redraw in-place to keep layout stable
        self.ax.clear()
        try:
            if self.mode.get() == "zoom":
                draw_zoom(shape, ax=self.ax)
            else:
                # prefer API that accepts ax; if your version returns (fig,ax), draw again onto our ax
                out = draw_shape_full(shape, ax=self.ax)
                # some versions may return (fig, ax); ignore result—we already drew into self.ax
        except TypeError:
            # Fallback: newer draw_shape_full may not accept ax; draw then copy image (rare). Simpler: warn.
            self.ax.text(0.5, 0.5, "Update render/fretboard_full.py to accept ax=...", ha="center")
        self.canvas.draw()
        self._update_status()

    # ---------- NAV ----------
    def next(self):
        if not self.names: return
        self.idx = (self.idx + 1) % len(self.names)
        self._render()

    def prev(self):
        if not self.names: return
        self.idx = (self.idx - 1) % len(self.names)
        self._render()

    # ---------- AUTOPLAY ----------
    def start_autoplay(self):
        if not self.names:
            messagebox.showinfo("Autoplay", "No chords to play.")
            return
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self._schedule_next()

    def stop_autoplay(self):
        if self._autoplay_job is not None:
            self.after_cancel(self._autoplay_job)
            self._autoplay_job = None
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def _schedule_next(self):
        delay_ms = max(50, int(self.period_s.get() * 1000))
        self._autoplay_job = self.after(delay_ms, self._tick)

    def _tick(self):
        if not self.names:
            self.stop_autoplay()
            return
        if self.randomize.get():
            self.idx = random.randrange(len(self.names))
        else:
            self.idx = (self.idx + 1) % len(self.names)
        self._render()
        self._schedule_next()

    # ---------- SELECTION ----------
    def _apply_custom(self):
        items = [s.strip() for s in self.custom_list.get().split(",") if s.strip()]
        if not items:
            messagebox.showinfo("Custom", "Type chords separated by commas, e.g. C, Dm, G7")
            return
        self.names = self._pick_names("custom", custom_list=items)
        self.idx = 0
        self._render()

    def _on_set_change(self, _event=None):
        choice = self.current_set.get()
        self.names = self._pick_names(choice)
        self.idx = 0
        self._render()

    def _pick_names(self, selection="all", custom_list=None):
        # prefer your select helper if available
        if _select:
            if selection == "custom" and custom_list:
                # let select_chords filter the valid ones
                valid = [n for n in custom_list if n in self.shapes_by_name]
                return valid
            return _select(self.shapes_by_name, self.meta_by_name, self.sets, selection)

        # fallback heuristics
        names = sorted(self.shapes_by_name.keys())
        if selection == "custom" and custom_list:
            return [n for n in custom_list if n in self.shapes_by_name]
        if selection == "major":
            return [n for n in names if not n.endswith("m")]
        if selection == "minor":
            return [n for n in names if n.endswith("m")]
        if selection == "all":
            return names
        # sets defined in YAML (simple support)
        if selection in self.sets:
            rule = self.sets[selection] or {}
            inc = rule.get("include")
            if inc == "*":
                return names
            if isinstance(inc, list):
                return [n for n in inc if n in self.shapes_by_name]
        return names

    # ---------- STATUS ----------
    def _update_status(self):
        mode = self.mode.get()
        sname = self.current_set.get()
        chord = self.names[self.idx] if self.names else "-"
        self.status.config(text=f"Set: {sname} | Mode: {mode} | Chord: {chord} ({self.idx+1}/{len(self.names)})")


def main():
    app = CavacoHeroTk()
    app.mainloop()


if __name__ == "__main__":
    main()
