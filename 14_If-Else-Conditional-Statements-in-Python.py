a=int(input("enter your age "))
print("your age is:",a)

if(a>18):
    print("you can drive")
else:
    print("you can't drive")

num = int(input("enter your num "))

if(num < 0):
    print("number is negative")

elif(num > 0):
    if(num <= 10):
        print("num is less then 10")
    elif(num <= 20):
        print("num is less then 20")
    else:
        print("num is greator then 20")
else:
    print("i dont know wtf is num")