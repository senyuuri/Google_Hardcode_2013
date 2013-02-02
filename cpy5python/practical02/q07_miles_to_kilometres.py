#Name:q07_miles_to_kilometres.py
#Author:Zhan Yuli
#Description:Conversion from miles to kilometres
#Created:010213

for i in range(0,11):
    if i == 0:
        print("Miles Kilometers Kilometres Miles")
    else:
        print("{0:<5d}".format(i),"{0:<10.3f}".format((i)*1.609),"{0:<10d}".format(15+i*5),"{0:<.3f}".format((15+i*5)/1.609),)
