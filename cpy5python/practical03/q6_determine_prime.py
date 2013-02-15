#Name:q6_determine_prime.py
#Author:Zhan Yuli
#Description:Prime number
#Created:150213
import math

def is_prime(n):
    for i in range(2,int(math.sqrt(n))+1):
        if(n%i == 0):
            return False
    return True

count = 0
for i in range(2,1001):  
    if(is_prime(i)):
        if(count<9):
            print("{0:4d}".format(i),end="")
            count += 1
        else:
            print("{0:4d}".format(i))
            count = 0

