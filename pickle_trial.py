import pickle
import requests
response = requests.get('https://en.wikipedia.org/wiki/Richard_Feynman')
response_str = str(response)
print(response_str) 
f = open('response.txt', 'wb')
pickle.dump(str(response), f)
f.close()

