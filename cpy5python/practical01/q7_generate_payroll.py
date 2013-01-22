#Payroll
name = input("Enter name: ")
hour = int(input("Enter number of hours worked weekly: "))
payrate = float(input("Enter hourly pay rate: "))
cpf = int(input("Enter CPF contribution rate(%): "))


print("Payroll statement for ", name)
print("Number of hours worked in week: ", hour)
print("Hourly pay rate: $", payrate)
print("Gross pay = $", payrate * hour)
print("CPF contribution at %", cpf," = $", payrate*hour*cpf*0.01)
print("Net pay = $", payrate*hour - payrate*hour*cpf*0.01)
