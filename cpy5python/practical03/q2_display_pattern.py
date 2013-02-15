#Name:q2_display_pattern.py
#Author:Zhan Yuli
#Description:Displaying patterns
#Created: 150213

def display_pattern(n):
    s = []
    l = 0
    for j in range(1, n+1):
        s.append(" " + str(j))
        l = len("".join(s))       
    s = []
    for i in range(1, n+1):
        s.append(" " + str(i))
        print("{0:>s}".format(("".join(s[::-1]))).rjust(l))
        
display_pattern(10)
