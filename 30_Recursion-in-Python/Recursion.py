def factorial(n):
    if (n==0 or n==1 ):
        return 1
    else:
        return n * factorial(n-1)

print(factorial(5))

# how this function works
# 5*factorial(4)
# 5*4*factorial(3)
# 5*4*3*factorial(2)
# 5*4*3*2*factorial(1)
# 5*4*3*2*1

def fibo(n):
    if n==0 or n==1:
        return n
    else:
        return fibo(n-1)+fibo(n-2)
    

print(fibo(0))
print(fibo(1))
print(fibo(2))
print(fibo(3))

# f0= 0
# f1= 1
# f2= 1+0
# fn= f(n-1)+f(n-2)