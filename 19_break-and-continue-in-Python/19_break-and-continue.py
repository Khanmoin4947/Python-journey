# Breaking a fro loop
for i in range(12):
    print("5 x",i,"=",(5*i))
    if (i==10):
        break

print("Now i am outside the loop")

# Emulating a while Loop
q = 0
while True:
   print(q)
   q = q+1
   if (q%100==0):
      break