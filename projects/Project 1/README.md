# Message Encryptor

A Python program that encrypts plaintext messages by substituting each word with a SHA-256 hash key looked up from a CSV word list.

## How It Works

1. The user types a message at the console prompt.
2. The message is normalized — converted to lowercase and stripped of punctuation.
3. Each word in the message is looked up in `words_w_hash.csv`, which maps plain words to their SHA-256 hash values.
4. Any word found in the mapping is replaced with its hash. Words not in the dictionary are silently dropped.
5. The encrypted output (a list of hash strings) is printed to the console.

## Project Structure

```
Project 1/
    main.py             # Main program — takes input, runs encryption, prints output
    csvEditor.py        # One-time script that generates words_w_hash.csv from words.csv
    words.csv           # Source word list
    words_w_hash.csv    # Generated word-to-hash mapping used for encryption
```

## How to Run

1. Install dependencies:

```bash
pip install pandas
```

2. (First time only) Generate the hash mapping file:

```bash
python csvEditor.py
```

3. Run the encryptor:

```bash
python main.py
```

4. Type your message when prompted:

```
Type your message to be encrypted: hello world
['2cf24dba...', '486ea...']
```

## Example

Input:
```
hello world
```

Output (truncated for readability):
```
['2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', '486ea46224d1bb4fb680f34f7c9ad96a8f24ec88be73ea8e5a6c65260e9cb8a7']
```

## Notes

- Words not present in `words_w_hash.csv` are excluded from the output rather than passed through as plaintext.
- The hash function used is SHA-256 (via Python's `hashlib`). The same word always produces the same hash.
- `csvEditor.py` uses pandas and has a hardcoded file path — update `setwd` if running on a different machine.
