#Name:q6_sum_digits.py
#Author:Zhan Yuli
#Description:Summing the digits in an integer using recursion
#Created: 160213

def sum_digits(n):
    if n < 10:
        return n
    else:
        return (n%10)+sum_digits(n//10)


print(sum_digits(234))
