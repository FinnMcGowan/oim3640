# Word Pattern Analyzer: Code Outline

## Goal
Build a Python program that reads a text file, cleans the text, creates two-word pairs, counts repeated pairs with a dictionary, and prints the most common patterns.

## General Program Sections

### 1. Imports and Constants
Purpose: set up any modules and file paths used by the program.

Possible items:
- `import string`
- a constant for the input file path
- a constant for how many results to display

Example structure:
```python
import string

BOOK_FILE = "data/Pride and Prejudice.txt"
TOP_RESULTS = 20
```

### 2. Read the Text File
Purpose: open the file and return the full text as one string.

Function:
```python
def read_text_file(filename):
	"""Return the contents of a text file as a string."""
```

What it should do:
- open the file with `with open(...)`
- read the file contents
- return the text

### 3. Clean and Process the Text
Purpose: make the text easier to analyze.

Function:
```python
def clean_text(text):
	"""Convert text to lowercase and remove punctuation."""
```

What it should do:
- convert all letters to lowercase
- remove punctuation marks
- optionally remove extra spaces or line breaks
- return cleaned text

### 4. Split the Text into Words
Purpose: turn the cleaned text into a list of individual words.

Function:
```python
def get_words(text):
	"""Split cleaned text into a list of words."""
```

What it should do:
- use `.split()`
- return a list of words

### 5. Build Two-Word Pairs
Purpose: create patterns from neighboring words.

Function:
```python
def make_word_pairs(words):
	"""Create a list of adjacent two-word pairs."""
```

What it should do:
- loop through the word list
- combine `words[i]` and `words[i + 1]`
- store each pair in a list
- return the list of pairs

Example result:
- if the words are `['mr', 'darcy', 'was', 'silent']`
- the pairs would be `['mr darcy', 'darcy was', 'was silent']`

### 6. Count Pair Frequencies with a Dictionary
Purpose: count how many times each pair appears.

Function:
```python
def count_pairs(word_pairs):
	"""Return a dictionary mapping each pair to its frequency."""
```

What it should do:
- create an empty dictionary
- loop through each word pair
- add new pairs to the dictionary
- increase the count when a pair appears again
- return the dictionary

Dictionary format:
```python
{
	"mr darcy": 18,
	"lady catherine": 9,
	"young man": 14
}
```

### 7. Sort and Display the Results
Purpose: show the most common repeated patterns.

Function:
```python
def print_top_pairs(pair_counts, limit):
	"""Print the most common word pairs."""
```

What it should do:
- sort the dictionary by count from highest to lowest
- print the top results
- format the output clearly

Optional improvement:
- skip very common but uninteresting pairs if needed

### 8. Main Program Flow
Purpose: run all functions in the correct order.

Function:
```python
def main():
	"""Run the word pattern analysis program."""
```

Suggested order:
1. read the file
2. clean the text
3. split text into words
4. create word pairs
5. count the pairs
6. print the top results

Example skeleton:
```python
def main():
	text = read_text_file(BOOK_FILE)
	cleaned_text = clean_text(text)
	words = get_words(cleaned_text)
	word_pairs = make_word_pairs(words)
	pair_counts = count_pairs(word_pairs)
	print_top_pairs(pair_counts, TOP_RESULTS)


main()
```

## Minimum Functions Needed
- `read_text_file(filename)`
- `clean_text(text)`
- `get_words(text)`
- `make_word_pairs(words)`
- `count_pairs(word_pairs)`
- `print_top_pairs(pair_counts, limit)`
- `main()`

## Possible Extra Features Later
- ignore stopwords like "the" and "and"
- remove Project Gutenberg header text
- let the user choose the input file
- compare word pairs across two different books
- save results to a new text file

## Suggested Build Order
1. Read and print a small sample of the file.
2. Clean the text and test that punctuation is removed.
3. Split the text into words.
4. Build a short list of word pairs.
5. Count the pairs with a dictionary.
6. Sort and print the most common pairs.
7. Add optional improvements if the basic version works.
