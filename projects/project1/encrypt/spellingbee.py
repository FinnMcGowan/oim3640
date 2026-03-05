def uses_only(word, letters):
    """Does word use only the allowed letters?"""
    for letter in word:
        if letter not in letters:
            return False
    return True 

def is_valid(word, letters, required):
    """Is word valid: does it use only the allowed letters and contain the required letter and at least 4 letters long?"""
    if not required in word:
        return False
    if len(word) < 4:
        return False
    return uses_only(word, letters)

def find_words(letters, required):
    """Print all valid words."""
    valid_words = []
    with open("data/words.txt") as word_file:
        for word in word_file:
            word = word.strip()
            if is_valid(word, letters, required):
                valid_words.append(word)
    
    return valid_words

def main():
    """Loads words, set up puzzle, print results"""
    word_list = find_words("kcboela", "a")
    print(word_list)

if __name__ == "__main__":
    main()
