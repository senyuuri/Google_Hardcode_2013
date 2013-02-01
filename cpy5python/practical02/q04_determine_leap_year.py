#Name:q04_determine_leap_year.py
#Author:Zhan Yuli
#Description:Determining leap year
#Created:010213

year = int(input("Enter year:"))
if (year % 4 == 0 and year % 100 != 0):
  print("Leap")
elif year % 400 ==0:
  print("Leap")
else:
  print("Non-Leap")
