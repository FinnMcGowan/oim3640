import string

BOOK_FILE = "data/Pride and Prejudice.txt"
TOP_RESULTS = 20

def read_text_file(filename):
    """Return the contents of a text file as a string."""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def clean_text(text):
    """Convert text to lowercase and remove punctuation."""
    text = text.lower()
    return text.translate(str.maketrans('', '', string.punctuation))

def get_words(text):
    """Split cleaned text into a list of words."""
    return text.split()

def make_word_pairs(words):
    """Create a list of adjacent two-word pairs."""
    return [f"{words[i]} {words[i + 1]}" for i in range(len(words) - 1)]

def count_pairs(word_pairs):
    """Return a dictionary mapping each pair to its frequency."""
    pair_counts = {}
    for pair in word_pairs:
        if pair in pair_counts:
            pair_counts[pair] += 1
        else:
            pair_counts[pair] = 1
    return pair_counts

def print_top_pairs(pair_counts, limit):
    """Print the most common word pairs."""
    sorted_pairs = sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)
    print("Most Common Word Pairs:")
    for pair, count in sorted_pairs[:limit]:
        print(f"{pair}: {count}")

def main():
    """Run the word pattern analysis program."""
    text = read_text_file(BOOK_FILE)
    cleaned_text = clean_text(text)
    words = get_words(cleaned_text)
    word_pairs = make_word_pairs(words)
    pair_counts = count_pairs(word_pairs)
    print_top_pairs(pair_counts, TOP_RESULTS)

if __name__ == "__main__":
    main()
