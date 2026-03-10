a = [1, 2, 3]
b = a
b.append(4)
print(a, b) # a is the same as b, because they now reference the same list object in memory (id(a) == id(b))
print(a is b)

names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 95]
name_scores = list(zip(names, scores))
print(name_scores) # [('Alice', 85), ('Bob', 90), ('Charlie', 95)]
print(name_scores[2][1])

eng2sp = {'one': 'uno', 'two': 'dos', 'three': 'tres', 'four': 'cuatro'}
for k in eng2sp:
    print(k)

for eng in eng2sp:
    sp = eng2sp[eng]
    if sp == 'dos':
        print(eng)


for k, v in eng2sp.items():
        print(k, v)

def histogram(s):
    d = {}
    for c in s:
        if c not in d:
            d[c] = 1
        else:
            d[c] += 1       
    return d
