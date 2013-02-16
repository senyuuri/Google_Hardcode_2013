#Name:q7_find_largest.py
#Author:Zhan Yuli
#Description:Finding the largest number in an array
#Created: 160213

l = -100000

def find_largest(alist):
    global l
    if(len(alist)==1):
        if alist[-1]>l:
            l = alist[-1]
            return l
        else:
            return l
    else:
        if alist[-1]>l:
            l = alist[-1]
        return(find_largest(alist[:(len(alist)-1)]))
            

alist=[5,1,8,7,2]
print(find_largest(alist))
