import requests
import json

testUrl = 'http://localhost:8090/test'
headers = {'content-type': 'application/json'}

url = 'http://172.17.0.2:80/'
# tests = [
# 	'v1_module_mnist',
# 	'v1_module_fashion-mnist',
# 	'v2_module_mnist',
# 	'v2_module_fashion-mnist'
# ]
tests = [
	'v2_integration'
]

response = requests.post(testUrl, json={'url': url, 'tests': tests}, headers=headers)
response_json = json.loads(response.text)

print(response_json['report'])