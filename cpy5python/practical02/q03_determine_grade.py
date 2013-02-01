#Name:q03_determine_grade.py
#Author:Zhan Yuli
#Description:Determining grade
#Created:300113

s = int(input("Enter score:"))
if 70<= s <= 100:
    print("A")
elif 60<= s <= 69:
    print("B")
elif 55<= s <= 59:
    print("C")
elif 50<= s <= 54:
    print("D")
elif 45<= s <= 49:
    print("E") 
elif 35<= s <= 44:
    print("S")
elif 0 <= s <= 35:
    print("U")
else:
    print("Invalid! Score must be within 0 - 100.")
            
