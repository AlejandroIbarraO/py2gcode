Py2Gcode
========

This package was debeloped to produce for non conventional aplications. Especialy the control of printers with seringe pump extruders. This debelopment was heavily influenced by the mecode library (if you see some resamblens) by jminardi. And other inspiration was the turtle style of coding, so you give the intruction of moving to the head coordinate by coordinate. 

In this implemenetation the main focus is produce direcctly the gcode after every passed command, and also keep track of nozzle position and amount of material extruded.

The usage of this package is not restricted to seringe pump based printers, in more general sense is a interface between python and Gcode. Also many examples directly write some comands in gcode format (pased by a write funtion), this is because some Gcode flavors have differnts commands for specials feaures. 

IMPORTANT: All the units are in mm !!!

Quick start
-----------
To start we have to initiate the library calling py2gcode. The two important parametres to initalize this pachage are the initial diameter of your material and the desired diameter of the filament exiting the nozzle. 

```python 
from py2gcode import py2gcode
# lets cretate a triangular path
# set the initial diameter of the material and the output diameter.
pg = py2gcode(material_diameter = 8.6,nozzle_diameter = 0.91) 
pg.go_home()

pg.move_abs(z = 10.0) # rise the nozzle 10.0 [mm]

pg.move_abs(x = 10.0,y = 10.0)

pg.move_abs(z = 0.2) # move sligly adove the surface
# triangular profile using relative movements
pg.move(x = 5.0,y = 10.0, extrude = True)
pg.move(x = 5.0,y = -10.0, extrude = True)
pg.move(x = -10, extrude = True)

pg.move_abs(z = 10.0) # safe position
pg.move_abs(x = 0)
pg.move_abs(y = 0)

pg.plot() # 3d representation using matplotlib
pg.out('mygcode') # generate the gcode file

```




