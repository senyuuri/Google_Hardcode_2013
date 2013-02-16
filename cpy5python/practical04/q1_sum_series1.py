#Name:q1_sum_series1.py
#Author:Zhan Yuli
#Description:Summing series
#Created: 150213

def sum_series1(n):
    if n == 1:
        return 1
    else:
        return ((1/n)+sum_series1(n-1))

print(sum_series1(5))
