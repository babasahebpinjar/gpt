import requests

url = 'http://localhost:5000/analyze'
data = {'text': 'This is a wat I love to do.'}

response = requests.post(url, json=data)

if response.ok:
    result = response.json()
    print(result)
else:
    print('Error:', response.status_code, response.reason)

