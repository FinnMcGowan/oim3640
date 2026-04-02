import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pprint import pprint


ENV_PATH = Path(__file__).parent / '.env'


def create_openai_client():
    load_dotenv(ENV_PATH)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY was not found in the .env file next to this script.")
    return OpenAI(api_key=api_key)





'''
api_key = input("Enter your OpenAI API key: ")
client = OpenAI(api_key=api_key)

numbers_input = input("Enter numbers to add, separated by spaces: ")
numbers = numbers_input.split()

prompt = f"Add these numbers together and give me only the numeric result: {' + '.join(numbers)}"

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print("Result:", response.choices[0].message.content)

# sends 2 numbers to ai and asks it to add them together, then prints the result.

'''
def get():
    #GET
    data = requests.get('https://oim.108122.xyz/messages').json()
    for msg in data:
        print(msg)

def post(msg):
    #POST
    requests.post('https://oim.108122.xyz/message',
                json={'message': msg},
                headers={'X-Token': 'finnfinn'})


def delete():
    # DELETE MESSAGE
    requests.delete('https://oim.108122.xyz/message/1',
                    headers={'X-Token': 'finnfinn'})



def GetWeather():
    load_dotenv(Path(__file__).parent / '.env')
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q=Boston&appid={API_KEY}&units=imperial"
    )

    try:
        data = requests.get(url).json()
        print(f'Boston: {data["main"]["temp"]}°F')
    except Exception as e:
        print("Error fetching weather data:", e)

#GetWeather()

def openai_example():
    client = create_openai_client()
    response = client.responses.create(
        model = 'gpt-5-nano', input="give me 10 random text faces"
    )
    print(response.output_text)

#openai_example()

# use openai key to make a new shell for an ai chatbot from this program(probably with a while loop)
try:
    client = create_openai_client()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[{"role": "user", "content": user_input}]
        )
        print("AI:", response.choices[0].message.content)
except ValueError as error:
    print(error)