# score = int(input("enter your score: "))
# if score >= 60:
#     print("You passed!")
# elif score >= 90:
#     print("You got an A!")
# else:    
#     print("You failed.")

# 1

def evaluate_score(score):
    if score >= 60:
        print("You passed!")
    elif score >= 90:
        print("You got an A!")
    else:    
        print("You failed.")

score = int(input("enter your score: "))
result = evaluate_score(score)
print(result)

# 2

def mystery(x):
    if x > 0:
        return "positive"
    print("done")   # Because "return" immediately exits the function, this line will only be executed if x is not greater than 0.
result = mystery(5)
print(result)

# 3

x = 15
y = x > 10 and x < 20
print(y)
print(type(y)) # Type = Bool, Value = True

# 4

def is_leap_year(year):
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    return False
print(is_leap_year(2020)) # True
print(is_leap_year(1900)) # False

# 5

def check(n):
    if n % 2 == 0:
        if n % 3 == 0:
            print("A")
        else:
            print("B")
    else:
        print("C")

check(8)
check(6)

