# We use while loops when we want to repeat until a condition becomes false.
# First loop
i = int(input("Enter your number: "))
while(i<=40):
     i = int(input("Enter your number: "))
     print(i)
print("loop is closed now")

# Second loop 
count = int(input("Enter your number: "))
while(count>0):
    print(count)
    count=count-1

# Use of else in loop
i = 5
while(i<0):
     print(i)
     i=i-1
else:
     print("now i am inside else")