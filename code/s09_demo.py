# for i in range(5):
#     print(i)

# while loops
# n = 0
# while n < 5:
#     print(n)
#     n += 1

# list
words = ["hello", "world", "target", "python"]

# Eg for "break"

# for w in words:
#     print('checking:', w)
#     if w == "target:":
#         print("found it!")
#         break

# eg for "continue"

# for w in words:
#     print('checking:', w)
#     if w == "target":
#         print("found it!")
#         continue
#     print("Not the target\n")


# for letter in 'Gadsby':
#     print(letter, end=' ')

for num in range(10):
    if num % 2 == 0:
        continue
    print(num)