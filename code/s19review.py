
# ValueError
try:
    x = int('not a number')
    print('success')
except ValueError:
    print('oops')
print('done')

# TypeError
try:
    x = 5 + '5'
    print('success')
except TypeError:
    print('oops')

