Py2Gcode
========

This package was developed to produce for non-conventional applications. Especially the control of printers with syringe pump extruders. This development was heavily influenced by the mecode library (if you see some resemblance) by jminardi. And other inspiration was the turtle style of coding, so you give the instruction of moving to the head coordinate by coordinate. 

In this implementation the main focus is produce directly the gcode after every passed command, and also keep track of nozzle position and amount of material extruded.

The usage of this package is not restricted to syringe pump based printers, in more general sense is a interface between python and Gcode. Also many examples directly write some commands in gcode format (passed by a write function), this is because some Gcode flavors have different commands for specials features. 

IMPORTANT: All the units are in mm !!!


Quick start
-----------
To start we have to initiate the library calling py2gcode. The two important parameters to initialize this package are the initial diameter of your material and the desired diameter of the filament exiting the nozzle.

```python 
from py2gcode import py2gcode
pg = py2gcode(material_diameter = 8.6,nozzle_diameter = 0.91)
pg =  
```




