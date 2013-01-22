#Payroll
name = input("Enter name: ")
hour = int(input("Enter number of hours worked weekly: "))
payrate = float(input("Enter hourly pay rate: "))
cpf = int(input("Enter CPF contribution rate(%): "))


print("Payroll statement for ", name)
print("Number of hours worked in week: ", hour)
print("Hourly pay rate: $", payrate)
print("Gross pay = $", payrate * 10)
print("CPF contribution at 20% = $", payrate*10*0.2)
print("Net pay = $", payrate*0.8)
