#Name:q3_find_gcd.py
#Author:Zhan Yuli
#Description:Computing GCD
#Created:150213

def cgd(m,n):
    i = 1
    cd = 1
    while(i < m and i < n):
        if(m % i == 0 and n % i == 0):
            cd = i
        i += 1
    print(cd)
    
cgd(24,16)
cgd(255,25)
