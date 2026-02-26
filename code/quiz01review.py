'''
def check(s):
    for c in s:
        if c.isupper():
            return True
        else:
            return False

print(check(s = "bALLS"))

#x = "StRing"
#print(x.isupper())
'''

flag = False

def check(s):
    for c in s:
        if c.isupper():
            return flag or True
        else:
            return False

print(check(s = "bALLS"))

#x = "StRing"
#print(x.isupper())

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    
    w