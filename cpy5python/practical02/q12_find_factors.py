#Name:q12_find_factors.py
#Author:Zhan Yuli
#Description:Finding the factors of an integer
#Created:010213


n = int(input("Enter an integer: "))
factor = []
f = 0
for i in range(2, n):
    while( n % i == 0):
        factor.append(i)
        n/= i

for i in range(0,len(factor)):
    if f == 0: print(factor[i], end = ""); f = 1
    else: print(",", factor[i], end = "")

        



