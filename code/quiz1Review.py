def check_uppercase(s):
    for c in s:
        result = 'c'.isupper() # some bs
    return result

def check_vowels(s):
    result_list = []
    for c in s:
        result = c in "aeiou"
        result_list.append(result)
    return result_list
 
def any_vowel(s):
    flag = False
    for c in s: 
        flag = flag or (c in 'aeiou')
    return flag

print(any_vowel('rythm'))
print(any_vowel('cafe'))
print(any_vowel('ski'))

# True or False = True
# False or True = True

# True and False = False
# False and True = False

def all_alpha(s):
    flag_list = []
    flag = True
    for c in s:
        flag = flag and c.isalpha()
        flag_list.append(flag)
    return flag_list

print(all_alpha('Babson'))
print(all_alpha('OIM3640'))
print(all_alpha('hello!'))

def has_space(s):
    for c in s:
        if c == ' ':
            break
            return True
    return False

print(has_space('ice cream'))
print(has_space(' hello'))
print(has_space('pizza'))

def all_digit(s):
    for c in s:
        if not c.isdigit():
            return False
    return True

print(all_digit('911'))
print(all_digit('3.14'))
print(all_digit('OIM3640'))
