# # Calls function from my file, koala.py
# import koala
# koala.koala(5)

# x = 3
# # prints int value, prints type name, typecasts value of int to str
# print(x, "x", str(x))

# def double(number):
#     # Doubles the input number and returns it
#     return number * 2

# print(double(5))
# print(double('5')) # This will concatenate the string '5' with itself 

# print("How does an \"escape character\" work?") # "\" creates an escape character


# # a = 5,   in python this means "assign 5 to variable a"
# a = 5 # int is immutable
# b = a
# a = 10
# print(a)
# print(b)

# a = [1, 2, 3] # list is mutable
# b = a # both reference the same list, rather than creating a copy
# a.append(4) # modifies list in place 
# print(b)
# print(a)

# # practice with local variables
# variable = 10
# def f():
#     message = 'Hello'
#     x = 5
#     return x
# y = f()
# print(y)
# #print(x)
# print(f())

# to comment out highlight lines and press Ctrl + /

# Draw a square
# to type emojis, press Windows + . (period)

"""
🧱🧱🧱🧱
🧱🧱🧱🧱
🧱🧱🧱🧱
🧱🧱🧱🧱
"""


# def draw_square(size):
#     for i in range(size): # for each row
#         print('🧱' * size) # size also determines the length of rows. (# of columns)

# draw_square(4)

# print('hi') # prints hi\n  (newline is default end character)
# print('hi', end=' ') # prints hi without newline

# def draw_square(size):
#     for i in range(size): # for each row
#         print('🧱' * size) # size also determines the length of rows. (# of columns)

# draw_square(4)


"""
create a function that draws a triangle
🧱          1 = 0 + 1
🧱🧱        2 = 1 + 1
🧱🧱🧱      3 + 2 + 1
🧱🧱🧱🧱    4 = 3 + 1
"""
# def draw_triangle(rows):
#     for i in range(rows): # for each row
#         print('🧱' * (i+1)) 

# def draw_triangle(rows):
#     for i in range(1, rows+1):
#         print('🧱' * i)

# draw_triangle(4)

"""
Draw a triangle like this (size = 5)
        i
    #   4 spaces + 1 # = 5  5 - 0 - 1 = 4
   ##   3 spaces + 2 # = 5  5 - 1 - 1 = 3
  ###   2 spaces + 3 # = 5  5 - 2 - 1 = 2
 ####   1 spaces + 4 # = 5  5 - 3 - 1 = 1
#####
"""

def hash_triangle(size):
    for i in range(size):
        print(" " * (size - i - 1) + "#" * (i + 1))

hash_triangle(5)

"""
Create a function that draws a pyramid
    #       4 spaces + 1 # = 5  5 - 0 - 1 = 4
   ###      3 spaces + 3 # = 6  5 - 1 - 1 = 3
  #####     2 spaces + 5 # = 7  5 - 1 - 2 = 2
 #######    1 spaces + 7 # = 8  5 - 1 - 3 = 1
"""
def draw_pyramid(size):
    for i in range(size):
        print(" " * (size - i - 1) + "#" * ())