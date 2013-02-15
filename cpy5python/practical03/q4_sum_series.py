#Name:q4_sum_series.py
#Author:Zhan Yuli
#Description:Summing series
#Created:150213

def m_series(i):
    s = 0
    print("i    m(i)")
    for j in range (1, i+1):
        s += (j/(j+1))
        print("{0:<5d}{1:.4f}".format(j,s))
    

m_series(20)
