"""04 - Archimedean spiral sampled at constant arc length.

A single continuous path (no retractions) that fills a disk. Constant
arc-length sampling keeps the segment length, and therefore the
extrusion per G1 line, uniform from the centre to the edge.
"""
import numpy as np
from _common import save
from py2gcode import py2gcode


def archimedean_spiral(turns, r0, ds, pitch):
    """Points of r = r0 + pitch/(2 pi) * theta spaced ds apart along the curve."""
    b = pitch / (2 * np.pi)
    theta, pts = 0.0, []
    while theta <= 2 * np.pi * turns:
        r = r0 + b * theta
        pts.append((r * np.cos(theta), r * np.sin(theta)))
        theta += ds / np.sqrt(r ** 2 + b ** 2)
    return np.array(pts)


Da = 2.0
cx, cy, z_work, z_safe = 60.0, 50.0, 1.0, 20.0
p2c = py2gcode(material_diameter=12.4, nozzle_diameter=Da)
p2c.feed, p2c.feednoprint = 300, 1000

# Printer-specific setup lines go through write(), e.g. a mixing ratio
# for a two-component head (Klipper macro used in the lab setup).
p2c.write("MIX_RATIO A=0.5 B=0.5")
p2c.write("G92 E0")

path = archimedean_spiral(turns=6, r0=10.0, ds=Da, pitch=Da)
p2c.move_abs(z=z_safe)
p2c.move_abs(x=cx + path[0, 0], y=cy + path[0, 1])
p2c.move_abs(z=z_work)
for x, y in path:
    p2c.move_abs(x=cx + x, y=cy + y, extrude=True)
p2c.move_abs(z=z_safe)
p2c.move_abs(x=0, y=0)

save(p2c, "04_archimedean_spiral", "Archimedean spiral")
