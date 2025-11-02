# old method

# letter="my name is {} and i am from {}"
letter="my name is {0} and i am from {1}"

name="moin"
country="india"

print(letter.format(name,country))

# new method(f-strings)
msg=f"my name is {name} and i am from {country}"
print(msg)

# to print as it is
msg2=f"my name is {{name}} and i am from {{country}}"
print(msg2)