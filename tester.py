import requests
import json
import yaml

testUrl = 'http://localhost:6000/test'
headers = {'content-type': 'application/json'}
tests = ['all']

response = requests.post(testUrl, json={'tests': tests}, headers=headers)
response_json = json.loads(response.text)
response_json_as_yaml = yaml.dump(response_json, default_flow_style=False, sort_keys=False)

print(response_json_as_yaml)