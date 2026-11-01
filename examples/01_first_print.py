"""01 - First print: purge lines and a filled square, two layers.

Shows the basic workflow: create the generator, travel with move_abs,
extrude with move (relative), retract/recover, then write the G-code.
"""
import numpy as np
from _common import save
from py2gcode import py2gcode

# Bead geometry. py2gcode treats the bead as a cylinder of diameter
# `nozzle_diameter`, so for a flat bead of width w and height h use the
# diameter with the same cross-section area: D = sqrt(4 w h / pi).
w, h = 0.41, 0.2                      # line width and layer height [mm]
Da = np.sqrt(4 * w * h / np.pi)

p2c = py2gcode(material_diameter=12.4,  # syringe / filament diameter [mm]
               nozzle_diameter=Da)
p2c.feed = 300                 # printing feed [mm/min]
p2c.feednoprint = 600          # travel feed [mm/min]
p2c.retraction_lenght = 0.25   # [mm of E]
p2c.retraction_speed = 100.0

x0, y0, z_safe = 20.0, 10.0, 5.0

p2c.write("G92 E0")                    # reset the extruder axis
p2c.move_abs(z=z_safe)
p2c.move_abs(x=x0, y=y0)
p2c.move_abs(z=h)
p2c.recover()

# Purge: three back-and-forth lines to get the flow going.
L = 15.0
for _ in range(3):
    p2c.move(x=L, extrude=True)
    p2c.move(y=w)
    p2c.move(x=-L, extrude=True)
    p2c.move(y=w)
p2c.retract()
p2c.move_abs(z=z_safe)

# Filled square, serpentine infill, two layers.
side = 10.0
start = (x0, y0 + 10.0)
p2c.move_abs(x=start[0], y=start[1])
p2c.move_abs(z=h)
p2c.recover()
for layer in range(2):
    direction = 1 if layer % 2 == 0 else -1
    for _ in range(int(side / (2 * w))):
        p2c.move(x=side, extrude=True)
        p2c.move(y=direction * w)
        p2c.move(x=-side, extrude=True)
        p2c.move(y=direction * w)
    p2c.move(z=h)                      # next layer
p2c.retract()
p2c.move_abs(z=z_safe)
p2c.move_abs(x=0, y=0)

save(p2c, "01_first_print", "Purge lines + filled square")
