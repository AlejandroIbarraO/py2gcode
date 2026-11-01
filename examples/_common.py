"""Small helpers shared by the examples (path setup and output folder)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # make the repo root importable

OUT = os.path.join(HERE, "output")
os.makedirs(OUT, exist_ok=True)


def save(p2c, name, title=None):
    """Write <name>.gcode and a 3D preview <name>.png into examples/output/."""
    import matplotlib.pyplot as plt

    p2c.output = os.path.join(OUT, name)
    p2c.out()
    fig, ax = p2c.plot()                       # built-in 3D preview
    if title:
        ax.set_title(title)
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=120, bbox_inches="tight")
    top_view(p2c, os.path.join(OUT, name + "_top.png"), title)
    length, volume = p2c.material_report()
    print(f"{name}.gcode: {len(p2c.command_history)} lines, "
          f"plunger travel {length:.2f} mm, volume {volume:.3f} mL")
    if "--show" in sys.argv:
        plt.show()
    plt.close(fig)


def top_view(p2c, path, title=None):
    """2D top view: extrusion moves in colour, travel moves faint."""
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    pos = p2c.position
    segs, colors, travel = [], [], []
    for i in range(len(pos["E"]) - 1):
        seg = [(pos["x"][i], pos["y"][i]), (pos["x"][i + 1], pos["y"][i + 1])]
        c = pos["E"][i + 1]
        if c in ("tab:blue", "tab:gray"):
            travel.append(seg)
        else:
            segs.append(seg)
            colors.append(c)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.add_collection(LineCollection(travel, colors="tab:blue", lw=0.4, alpha=0.25))
    ax.add_collection(LineCollection(segs, colors=colors, lw=0.9))
    pts = [p for s in segs for p in s] or [(0, 0)]
    xs, ys = zip(*pts)
    pad = 2
    ax.set_xlim(min(xs) - pad, max(xs) + pad)
    ax.set_ylim(min(ys) - pad, max(ys) + pad)
    ax.set_aspect("equal")
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    if title:
        ax.set_title(title)
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)
