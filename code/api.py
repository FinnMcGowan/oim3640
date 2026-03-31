import requests
import pprint # pretty print, for better readability of the output

### API 1, a random word generator

# response = requests.get('https://oim.108122.xyz/words/random')
# print(response.json()) # a random word!

### API 2, Massachussetts Town Data

response = requests.get('https://oim.108122.xyz/mass', headers = {'X-Token': 'finnfinn'}) # your first name twice
# live board of API requests: https://oim.108122.xyz/live
#pprint.pprint(response.json())
data = response.json()
print(len(data))
print(data.keys())
print(type(data['data'])) # do this for explore the data structure

towns = data['data'] # Towns is a list of dictionaries
print(len(towns)) # 351

# Find smallest population town in massachussetts
smallest_population = min(towns, key=lambda town: town['population'])
print(smallest_population)