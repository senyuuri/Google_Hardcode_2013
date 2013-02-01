#Name:q02_triangle.py
#Author:Zhan Yuli
#Description:Validating triangles and computing perimeter
#Created:300113

a1 = int(input("Enter side 1: "))
a2 = int(input("Enter side 2: "))
a3 = int(input("Enter side 3: "))
if(a1+a2>a3 and a2+a3>a1 and a1+a3>a2):
  print("Perimeter: ", a1+a2+a3)
else:
  print("Invaild triangle")
