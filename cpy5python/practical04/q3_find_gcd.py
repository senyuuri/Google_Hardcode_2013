#Name:q3_find_gcd.py
#Author:Zhan Yuli
#Description:Computing greatest common divisor using recursion
#Created: 150213

def gcd(m, n):
    if m < n:
        m = m + n
        n = m - n
        m = m - n
    if n == 0:
        return m
    else:
        return gcd(n, m%n)
    
print(gcd(24,16))
print(gcd(255,25))
