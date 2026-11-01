"""02 - Speed calibration grid.

Prints a 2 x 3 grid of small rectangles, each at a different feed rate,
to find the speed that gives the right line width for a material.
Also shows how to send printer-specific commands with write(), here a
Klipper output pin driving a UV light used to cure the ink.
"""
import numpy as np
from _common import save
from py2gcode import py2gcode

w, h = 0.41, 0.2
Da = np.sqrt(4 * w * h / np.pi)
p2c = py2gcode(material_diameter=12.4, nozzle_diameter=Da)
p2c.retraction_lenght = 0.25
p2c.retraction_speed = 100.0
p2c.feednoprint = 600


def light(level):
    """Klipper: set the PWM value (0..1) of the UV light pin."""
    p2c.write(f"SET_PIN PIN=UVpin VALUE={level}")


x0, y0, z_safe = 20.0, 10.0, 5.0
speeds = np.array([100, 200, 300, 400, 500, 600]).reshape(2, -1)  # mm/min
width, height, space, n_layers = 15.0, 5.0, 3.0, 3

p2c.write("G92 E0")
p2c.move_abs(z=z_safe)
for i in range(speeds.shape[0]):
    for j in range(speeds.shape[1]):
        p2c.write(f"; patch feed {speeds[i, j]} mm/min")
        p2c.move_abs(x=x0 + j * (width + space), y=y0 + i * (height + space))
        p2c.move_abs(z=h)
        p2c.recover()
        p2c.feed = speeds[i, j]
        light(0.1)
        for layer in range(n_layers):
            direction = 1 if layer % 2 == 0 else -1
            for _ in range(int(0.5 * height / w)):
                p2c.move(x=width, extrude=True)
                p2c.move(y=w * direction)
                p2c.move(x=-width, extrude=True)
                p2c.move(y=w * direction)
            p2c.move(z=h)
            p2c.move(y=-w * direction)
        light(0)
        p2c.retract()
        p2c.move_abs(z=z_safe)
p2c.move_abs(x=0, y=0)

save(p2c, "02_speed_calibration", "Feed-rate calibration grid")
