import string
import openai

# Constants
BOOK_FILE = "data/Pride and Prejudice.txt"
API_KEY = "your_openai_api_key_here"  # Replace with your actual API key

# Set up OpenAI API key
openai.api_key = API_KEY

def read_text_file(filename):
    """Return the contents of a text file as a string."""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def clean_text(text):
    """Convert text to lowercase and remove punctuation."""
    text = text.lower()
    return text.translate(str.maketrans('', '', string.punctuation))

def count_character_mentions(text, character_names):
    """Count how many times each character appears in the text."""
    counts = {name: 0 for name in character_names}
    words = text.split()
    for word in words:
        if word in counts:
            counts[word] += 1
    return counts

def get_character_info(character_name):
    """Fetch general information about a character using the OpenAI API."""
    prompt = f"Provide a brief description of the character {character_name}."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def main():
    """Run the character tracker program."""
    # Define the characters to track
    character_names = ["elizabeth", "darcy", "jane", "bingley", "wickham"]

    # Read and clean the text
    text = read_text_file(BOOK_FILE)
    cleaned_text = clean_text(text)

    # Count character mentions
    character_counts = count_character_mentions(cleaned_text, character_names)

    # Print character counts
    print("Character Mentions:")
    for name, count in character_counts.items():
        print(f"{name.capitalize()}: {count}")

    # Fetch and print character info
    print("\nCharacter Information:")
    for name in character_names:
        info = get_character_info(name)
        print(f"{name.capitalize()}: {info}")

if __name__ == "__main__":
    main()
