#Name:q5_count_letter.py
#Author:Zhan Yuli
#Description:Occurrences of a specified character in a string
#Created: 160213

from string import *
count = 0

def count_letter(string,ch):
    global count
    if (string.find(ch) != -1):
        count += 1
        p = string.find(ch)
        return count_letter(string[(p+len(ch)):],ch)
    else:
        return count
        

print(count_letter("Welcome","e"))
