#Name:q8_find_uppercase.py
#Author:Zhan Yuli
#Description:Finding the number of uppercase letters in a string
#Created: 160213

num = 0

def find_num_uppercase(string):
    global num
    if(len(string)==1):
        if(string[-1].isupper()):
            num += 1
            return num
        return num
    else:
        if(string[-1].isupper()):
            num += 1
        return(find_num_uppercase(string[:(len(string)-1)]))
    

print(find_num_uppercase('Good MorninG'))
