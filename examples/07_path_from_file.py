"""07 - Print a path stored in a .npz file, with per-point line width.

This is the format the lab notebooks use for patterns exported from
other tools (e.g. a polyline from PyVista / Blender):

    point       float array, shape (1, N, 3)  -> x, y, z of each vertex [mm]
    point_data  float array, shape (1, N)     -> line diameter at each vertex [mm]

If the file does not exist, a demo pattern (a rose curve whose width
varies along the path) is generated first.
"""
import os
import numpy as np
from _common import HERE, save
from py2gcode import py2gcode

pattern_path = os.path.join(HERE, "patterns", "demo_rose.npz")

if not os.path.exists(pattern_path):
    os.makedirs(os.path.dirname(pattern_path), exist_ok=True)
    t = np.linspace(0, 2 * np.pi, 1500)
    r = 25 * np.cos(3 * t)
    pts = np.stack([r * np.cos(t), r * np.sin(t), np.zeros_like(t)], axis=1)
    width = 0.6 + 0.6 * np.abs(np.cos(3 * t))        # thicker at the petal tips
    np.savez(pattern_path, point=pts[None], point_data=width[None])

pattern = np.load(pattern_path)
points = pattern["point"][0, :, :2]
diameters = pattern["point_data"][0]

# Centre the pattern on the build position and start from the lowest point.
center = np.array([60.0, 60.0])
points = points - points.mean(axis=0) + center
first = np.argmin(points[:, 1])
points, diameters = np.roll(points, -first, axis=0), np.roll(diameters, -first)

Da, z_work, z_safe = 1.0, 1.0, 15.0
p2c = py2gcode(material_diameter=12.4, nozzle_diameter=Da)
p2c.feed, p2c.feednoprint = 150, 1000
p2c.retraction_lenght, p2c.retraction_speed = 0.25, 100.0

p2c.write("G92 E0")
p2c.move_abs(z=z_safe)
p2c.move_abs(x=points[0, 0], y=points[0, 1])
p2c.move_abs(z=z_work)
p2c.recover()
for (x, y), d in zip(points[1:], diameters[1:]):
    p2c.line_diameter = d                # width of the segment ending here
    p2c.move_abs(x=x, y=y, extrude=True)
p2c.line_diameter = Da
p2c.retract()
p2c.move_abs(z=z_safe)
p2c.move_abs(x=0, y=0)

save(p2c, "07_path_from_file", "Path from .npz with variable width")
