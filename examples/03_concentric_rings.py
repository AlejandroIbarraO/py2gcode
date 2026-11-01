"""03 - Concentric rings with a radial line-width gradient.

Changing p2c.line_diameter between moves changes how much material is
extruded per mm. Here the width grows or shrinks with the radius to give
'dome', 'trumpet' or 'cone' profiles.
"""
import sys
import numpy as np
from _common import save
from py2gcode import py2gcode

shape = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "dome"

Da = 0.91          # nozzle diameter [mm]
pitch = 1.5        # distance between rings [mm]
r = np.arange(5.0, 30.0, pitch)
profile = {
    "dome": np.linspace(0.8, 1.2, len(r)),
    "trumpet": np.linspace(1.2, 0.8, len(r)),
    "cone": np.ones(len(r)),
}[shape]

cx, cy, z_work, z_safe = 50.0, 50.0, 1.0, 10.0
p2c = py2gcode(material_diameter=12.4, nozzle_diameter=Da)
p2c.feed, p2c.feednoprint = 300, 1000
p2c.retraction_lenght, p2c.retraction_speed = 0.25, 100.0

p2c.write("G92 E0")
p2c.move_abs(z=z_safe)
p2c.move_abs(x=cx + r[0], y=cy)
p2c.move_abs(z=z_work)
p2c.recover()
for ri, k in zip(r, profile):
    p2c.line_diameter = k * Da
    ds = 2 * Da                          # chord length of each segment
    t = np.arange(0, 2 * np.pi, ds / ri)
    for ti in t:
        p2c.move_abs(x=cx + ri * np.cos(ti), y=cy + ri * np.sin(ti), extrude=True)
p2c.line_diameter = Da
p2c.retract()
p2c.move_abs(z=z_safe)
p2c.move_abs(x=0, y=0)

save(p2c, f"03_concentric_rings_{shape}", f"Concentric rings ({shape})")
