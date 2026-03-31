freq = {'a': 3, 'b': 1, 'c': 2}
result = sorted(freq.items(), key=lambda x: x[1])
print(result)

# same as 
def sort_by_value(item):
    return item[1]

result = sorted(freq.items(), key=sort_by_value)
print(result)
