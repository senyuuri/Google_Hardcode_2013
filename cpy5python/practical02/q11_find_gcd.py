#Name:q11_find_gcd.py
#Author:Zhan Yuli
#Description:Computing the greatest common divisor
#Created:010213

n1 = int(input("Enter integer n1: "))
n2 = int(input("Enter ingeger n2: "))
if n1 > n2: m = n2
else: m = n1
for i in range(m, 0, -1):

    if n1 % i == 0 and n2 % i == 0:
         print("Greatest common divisor:", i)
         break
