#Name:q5_compute_series.py
#Author:Zhan Yuli
#Description:Computing series
#Created: 150213

def m_series(i):
    s = 4.0
    print("i    m(i)")
    for j in range(1,i+1):
        if(j%2 == 0):
            s += 4*(1/(2*j+1))
        else:
            s -= 4*(1/(1+2*j))
            print("{0:<5d}{1:.11f}".format(j,s))   
        
m_series(19)
