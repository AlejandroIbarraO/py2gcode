"""05 - Hilbert curve infill.

hilbert_curve.py builds the curve as an L-system and turns it into unit
step vectors; each step becomes one relative extrusion move.
"""
import numpy as np
from _common import save
from py2gcode import py2gcode
import hilbert_curve

Da = 1.5
step = 1.5 * Da                  # length of one curve segment [mm]
order = 4                        # 2**order x 2**order cells

p2c = py2gcode(material_diameter=12.4, nozzle_diameter=Da)
p2c.feed = 300
p2c.write("G92 E0")
p2c.move_abs(z=10.0)
p2c.move_abs(x=25.0, y=10.0)
p2c.move_abs(z=0.7)

vectors = hilbert_curve.translate(hilbert_curve.hilbert_curve(order), output="vectors")
for vx, vy in vectors[1:]:       # the first entry is the (0, 0) origin
    p2c.move(x=vx * step, y=vy * step, extrude=True)

p2c.move_abs(z=10.0)
p2c.move_abs(x=0, y=0)
save(p2c, "05_hilbert_curve", f"Hilbert curve, order {order}")
