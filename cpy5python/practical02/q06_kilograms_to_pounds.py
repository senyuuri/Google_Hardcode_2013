#Name:q06_kilograms_to_pounds.py
#Author:Zhan Yuli
#Description:Conversion from kilograms to pounds
#Created:010213

for i in range(0,11):
   if i == 0:
     print("Kilograms Pounds")
   else:
     print("{0:<9d}".format(i),"{0:.1f}".format(i * 2.2))
