# Cavaco Hero

Cavaco Hero is an interactive tool for studying cavaco (Brazilian cavaquinho) chords. It displays chord shapes as vertical fretboard diagrams—either zoomed-in (focused on the chord) or full neck—and lets you navigate manually, autoplay through chord sets, or run in a slick Tkinter interface.

---

##  Features

- **Chord library** organized by quality and tags (major, minor, seventh).
- **Two views**:
  - **Zoomed mode**: auto-zooms around the chord.
  - **Full-neck**: entire fretboard from nut to `max_fret`.
- **CLI interface**:
  - Navigate (`n`, `p`) or jump to modes (`mode zoom`, `mode full`).
  - Select chord sets: `all`, `major`, `minor`, `sevenths`, custom sets from CLI or YAML.
  - Autoplay with configurable delay, random order toggle.
- **Tk interface** (coming soon!):
  - Embedded plot, dropdowns for mode/set, autoplay controls, and more.

---

##  Installation & Setup (CLI)

### Prerequisites

- Python **3.10+** (3.11 recommended)
- (Optional) `venv` for isolation

### Setup

```bash
git clone https://github.com/tuliofalmeida/cavaco_hero.git
cd cavaco_hero
python -m venv .venv
source .venv/bin/activate    
pip install --upgrade pip
pip install -e .
