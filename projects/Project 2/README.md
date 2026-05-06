# Word Pattern Analyzer

A Python program that reads a text file and finds the most common two-word phrases (bigrams) using dictionaries and string processing.

## How It Works

1. Reads the full text of a book from a `.txt` file.
2. Cleans the text — converts to lowercase and strips all punctuation.
3. Splits the cleaned text into individual words.
4. Builds adjacent two-word pairs (bigrams) from every neighboring word in the list.
5. Counts how many times each pair appears using a dictionary.
6. Prints the top 20 most frequent word pairs, sorted by count.

## Project Structure

```
Project 2/
    wordPatters.py      # Main program with all functions and analysis logic
    PROPOSAL.MD         # Original project proposal
data/
    Pride and Prejudice.txt   # Source text used for analysis (referenced by relative path)
```

> Note: the program expects to be run from the repository root so the relative path `data/Pride and Prejudice.txt` resolves correctly.

## How to Run

No external dependencies — uses only the Python standard library.

```bash
python "projects/Project 2/wordPatterns.py"
```

Run from the repository root:

```
public-repository/
```

## Example Output

```
Most Common Word Pairs:
of the: 491
to be: 282
in the: 264
it was: 234
i am: 216
...
```

## Functions

| Function | Description |
|---|---|
| `read_text_file(filename)` | Reads and returns the full text of a file |
| `clean_text(text)` | Lowercases and removes all punctuation |
| `get_words(text)` | Splits cleaned text into a word list |
| `make_word_pairs(words)` | Builds a list of adjacent two-word pairs |
| `count_pairs(word_pairs)` | Counts frequency of each pair in a dictionary |
| `print_top_pairs(pair_counts, limit)` | Prints the top N pairs sorted by frequency |
| `main()` | Orchestrates the full analysis pipeline |

## Configuration

Two constants at the top of `wordPatters.py` can be changed without modifying any logic:

| Constant | Default | Description |
|---|---|---|
| `BOOK_FILE` | `data/Pride and Prejudice.txt` | Path to the text file to analyze |
| `TOP_RESULTS` | `20` | Number of top word pairs to display |
