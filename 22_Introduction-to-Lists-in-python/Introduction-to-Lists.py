marks = [3, 5, 6, "Harry", True, 6, 7 , 2, 32, 345, 23]
print(marks)

print(marks[0]) #list indexing
print(marks[1])
print(marks[2])
print(marks[3])
print(marks[4])
print(marks[3])

print(marks[-8]) #negative index

print(marks[3:12]) #jump index
print(marks[3:7:2])
print(marks[3:7:3])

# conditional statement on list
if 7 in marks:
    print("yes")
else:
    print("no")
#same thing applies for strings
if "ha" in "harry":
    print("yes")

# conditional statement IN list
lst=[i for i in range(10)]
print(lst)

lst=[i for i in range(10) if i%2==0]
print(lst)