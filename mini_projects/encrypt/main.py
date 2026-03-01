

import csv
import os
import string


def message(x):
    # accept any input, ensure it's a string
    if not isinstance(x, str):
        x = str(x)

    # normalize: lowercase and strip punctuation
    x = x.lower()
    translator = str.maketrans('', '', string.punctuation)
    x = x.translate(translator)

    words = x.split()

    # load mapping from words(1).csv
    mapping = {}
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
