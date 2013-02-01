#Name:q2_calc_cylinder_volume.py
#Author:Zhan Yuli
#Description:Computing the volume of a cylinder
#Created:220113

import math
r = float(input("Radius:"))
l = float(input("Length:"))
a = r*r*math.pi
v = a*l
print("Area:","{0:.2f}".format(a))
print("Volume:","{0:.2f}".format(v))
