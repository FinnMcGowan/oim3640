import string


BOOK_FILE = "data/Pride and Prejudice.txt"
TOP_RESULTS = 20


def read_text_file(filename):
	"""Return the contents of a text file as a string."""
	# Open the file, read all text, and return it.
	pass


def clean_text(text):
	"""Convert text to lowercase and remove punctuation."""
	# Lowercase the text and remove punctuation using string.punctuation.
	# Return the cleaned text.
	pass


def get_words(text):
	"""Split cleaned text into a list of words."""
	# Split the text into individual words and return the list.
	pass


def make_word_pairs(words):
	"""Create a list of adjacent two-word pairs."""
	# Combine neighboring words into pairs such as "mr darcy".
	# Return a list of strings.
	pass


def count_pairs(word_pairs):
	"""Return a dictionary mapping each pair to its frequency."""
	# Use a dictionary to count how many times each pair appears.
	pass


def print_top_pairs(pair_counts, limit):
	"""Print the most common word pairs."""
	# Sort the dictionary from highest count to lowest count.
	# Print the top results in a clear format.
	pass


def main():
	"""Run the word pattern analysis program."""
	# Suggested order:
	# 1. Read the file.
	# 2. Clean the text.
	# 3. Split the text into words.
	# 4. Create word pairs.
	# 5. Count the pairs.
	# 6. Print the top results.
	pass


if __name__ == "__main__":
	main()
