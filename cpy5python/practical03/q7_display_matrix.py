#Name:q7_display_matrix.py
#Author:Zhan Yuli
#Description:Displaying matrix of 0s and 1s
#Created:150213

import random

def print_matrix(n):
    for i in range (0, n):
        for j in range (0, n):
            if(j == n-1):
                print(random.randint(0,1))
            else:
                print(random.randint(0,1),end = " ")


print_matrix(3)
