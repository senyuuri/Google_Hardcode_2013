#Name:q08_top2_scores.py
#Author:Zhan Yuli
#Description:Finding the two highest scores
#Created:010213

num = int(input("Enter the number of students: "))
fir = -10000
sec = -10000

for i in range (0, num):
    name =  input("Enter name: ")
    score = int(input("Enter score: "))
    if score > fir:
        sec = fir
        n2 = n1
        fir = score
        n1 = name
        
    if score < fir and score > sec:
        sec = score
        n2 = name

print("Highest score: ", n1, fir)
print("Second highest score: ", n2, sec)
