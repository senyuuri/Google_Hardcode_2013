#Name:q05_find_month_days.py
#Author:Zhan Yuli
#Description:Finding the number of days in a month
#Created:010213

import calendar
month = int(input("Enter month: "))
year = int(input("Enter year: "))
print("Number of days: ", calendar.monthrange(year,month)[1])
