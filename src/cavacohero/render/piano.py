import matplotlib.pyplot as plt

def plot_chord(chord):
    name, tones = chord
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(name)
    # placeholder visualization: list tones
    ax.text(0.1, 0.5, ", ".join(tones), transform=ax.transAxes)
    ax.axis("off")
    return fig