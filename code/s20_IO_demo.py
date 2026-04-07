

def main():
    '''
    key:
    w = write (overwrites existing content)
    a = append (adds to end of file)
    r = read (default mode)
    '''
    #read_file()
    #write_file('data/s20_output.txt', "This is some new text.\n", 'w')




def read_file():
    # Read entire file
    with open('data/s20.txt') as f:
        text = f.read() # reads the whole file as a single string
        #text = f.readline() # reads one line at a time, returns a string with \n at the end
        #text = f.readlines()  # returns a list of lines
        print(text)

    # Read line by line (best for large files)
    with open('data/s20.txt') as f:
        for line in f:
            print(line.strip())  # strip() removes \n

def write_file(file, text, mode):
    # Write to file ('w' = overwrite, 'a' = append)
    with open(file, mode) as f:
        f.write(text)



# CSV / Excel
import csv

# Read CSV (each row becomes a dict)
with open('data/students.csv') as f:
    for row in csv.DictReader(f):
        print(f"{row['name']}: {row['grade']}")

# Write CSV
data = [{'name': 'Alice', 'grade': 95},
        {'name': 'Bob', 'grade': 87}]
with open('output.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'grade'])
    writer.writeheader()
    writer.writerows(data)