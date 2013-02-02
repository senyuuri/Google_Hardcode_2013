#Name:q10_find_largest.py
#Author:Zhan Yuli
#Description:Finding the largest n such that n3 < 12000
#Created:010213

n = 0
p = 1
while(p < 12000):
    n += 1
    p = n*n*n

print("The largest n such that n^3<12000:",  n - 1)
