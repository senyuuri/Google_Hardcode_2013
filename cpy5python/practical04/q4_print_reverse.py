#Name:q4_print_reverse.py
#Author:Zhan Yuli
#Description:Reverse the digits in an integer recursively
#Created: 150213

def reverse_int(n):
    if n < 10:
        print(n)
    else:
        print(n%10,end="")
        return reverse_int(n//10)

reverse_int(12345)
