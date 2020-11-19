import requests

testUrl = 'http://localhost:6000/test'
headers = {'content-type': 'application/json'}
datasets = ['MNIST', 'FashionMNIST', None]
response = requests.post(testUrl, json={'datasets': datasets}, headers=headers)
print('response json:', response.text)