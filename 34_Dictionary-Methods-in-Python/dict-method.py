dict1={101:25,102:26,103:46,104:49 }
dict2={105:39, 106:50}

# add all values of dict2 into dict1
dict1.update(dict2)
print(dict1)

# clear the full dictionary
dict2.clear()
print(dict2)

# remove a specific key and value pair using key
dict1.pop(101)
print(dict1)

# remove the last key value pair
# dict1.popitem()

