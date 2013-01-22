#Summing the digits in an integer
a = int(input("Please enter a number between 0 and 1000: "))
sum = a//100 + a%10 + a//10%10
print("Sum of all digits:", sum)
