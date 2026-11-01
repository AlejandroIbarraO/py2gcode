"""06 - Hatched squares with a layer-by-layer twist.

lines_pattern.generate_consecutive_hatch_lines() fills a square with
parallel lines at any angle, already ordered as a zig-zag. Rotating the
angle a little on every layer gives a twisted (cholesteric-like) stack;
four samples go from 0 to 90 degrees of total twist.
"""
import numpy as np
from _common import save
from py2gcode import py2gcode
from lines_pattern import generate_consecutive_hatch_lines

w, h = 0.84, 0.2
Da = np.sqrt(4 * w * h / np.pi)
side, n_layers, z0, z_safe = 20.0, 5, 0.2, 10.0
total_twist = np.linspace(0, 90, 4)          # degrees, one value per sample
origins = [(30, 20), (53, 20), (30, 43), (53, 43)]

p2c = py2gcode(material_diameter=12.4, nozzle_diameter=Da)
p2c.feed, p2c.feednoprint = 90, 1000
p2c.write("G92 E0")
p2c.move_abs(z=z_safe)

for twist, (ox, oy) in zip(total_twist, origins):
    for i, angle in enumerate(np.linspace(0, twist, n_layers)):
        segments = generate_consecutive_hatch_lines(side, w, angle)
        if i % 2:
            segments = segments[::-1]        # start where the last layer ended
        p2c.move_abs(x=ox + segments[0][0][0], y=oy + segments[0][0][1])
        p2c.move_abs(z=z0 + i * h)
        for (xa, ya), (xb, yb) in segments:
            p2c.move_abs(x=ox + xa, y=oy + ya)
            p2c.move_abs(x=ox + xb, y=oy + yb, extrude=True)
    p2c.move_abs(z=z_safe)
p2c.move_abs(x=0, y=0)

save(p2c, "06_hatch_twist", "Hatch infill with 0-90 deg twist")
