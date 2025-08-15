# print('hello')


# x = int(input("Enter the value of x: "))
# # x is the variable to match
# match x:
#     # if x is 0
#     case 0:
#         print("x is zero")
#     # case with if-condition
#     case 4:
#         print("case is 4")

#     case _ if x!=90:
#         print(x, "is not 90")
#     case _ if x!=80:
#         print(x, "is not 80")
#     case _:
#         print(x)




x = int(input("Enter your number:"))

match x:
    case 1:
        print("your number is 1")
    
    case _ if x!=34:
        print("number is not 34")
    
    case _:
        print(x, "is ypur number")
    