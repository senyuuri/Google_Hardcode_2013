#Name:q09_find_smallest.py
#Author:Zhan Yuli
#Description:Finding the smallest n such that n2 > 12000
#Created:010213

n = 0
p = 1
while(p < 12000):
    n += 1
    p = n*n   
print("The smallest n such that n^2>12000:", n)
