import time
from ..engine.state import AppState
from ..engine.scheduler import Scheduler
from ..render.piano import plot_chord

def run_cli():
    state = AppState()             # default settings
    sched = Scheduler(state)

    print("CavacoHero CLI — n: next, p: prev, r: random, t: toggle timer, q: quit")
    try:
        while True:
            if state.timer_enabled and sched.tick_if_due():
                state.next_chord()

            cmd = input("> ").strip().lower()
            if cmd == "q":
                break
            elif cmd == "n":
                state.next_chord()
            elif cmd == "p":
                state.prev_chord()
            elif cmd == "r":
                state.random_chord()
            elif cmd == "t":
                state.timer_enabled = not state.timer_enabled
                print(f"timer_enabled = {state.timer_enabled}")
            else:
                print("commands: n p r t q")

            fig = plot_chord(state.current_chord())
            fig.show()  # for now; Tk UI will embed later
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
