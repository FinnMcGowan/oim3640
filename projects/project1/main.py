

import csv # this imports the csv module, which provides functionality to read from and write to CSV files
import os # this imports the os module, which provides a way of using operating system dependent functionality, such as file path manipulation
import string # this imports the string module, which contains a collection of string constants, including punctuation characters


def message(x):
    # accept any input, ensure it's a string
    if not isinstance(x, str):
        x = str(x)

    # normalize: lowercase and strip punctuation
    x = x.lower()
    translator = str.maketrans('', '', string.punctuation) # this creates a translation table that maps all punctuation characters to None
    x = x.translate(translator)

    words = x.split() # this splits the normalized string into a list of words based on whitespace

    # load mapping from words(1).csv
    mapping = {} #this is a dictionary that will hold the mappings from the CSV file
    csv_path = os.path.join(os.path.dirname(__file__), 'words(1).csv')
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            # check for header row
            header = next(reader, None)
            if header and header[0].lower() == 'aa' and header[1].lower() == 'key':
                # header present, continue to data
                pass
            else:
                # first row was actual data
                if header:
                    mapping[header[0]] = header[1]
            for row in reader:
                if len(row) >= 2:
                    mapping[row[0]] = row[1]
    except FileNotFoundError:
        print(f"CSV file not found: {csv_path}")

    result = []
    for w in words:
        key = mapping.get(w)
        if key is not None:
            result.append(key)
    return result


if __name__ == '__main__':
    x = input("Type your message to be encrypted: ")
    encrypted = message(x)
    print(encrypted)
