import requests
import json

testUrl = 'http://localhost:8080/test'
headers = {'content-type': 'application/json'}

url = 'http://172.17.0.2:80/'
tests = ['v1_module_fashion-mnist']

response = requests.post(testUrl, json={'url': url}, headers=headers)
response_json = json.loads(response.text)

print(response_json['report'])