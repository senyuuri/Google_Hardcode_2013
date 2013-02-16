#Name:q1_sum_series1.py
#Author:Zhan Yuli
#Description:Summing series
#Created: 150213

def sum_series2(i):
    if i==0:
        return 1/3
    else:
        return ((i/(2*i+1))+sum_series2(i-1))


print(sum_series2(6))
