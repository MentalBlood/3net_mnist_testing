from flask import Flask, request
from flask_restful import Api, Resource
app = Flask(__name__)
api = Api(app)

import images_loader
images = images_loader.loadImages()

import test_runner

@app.route('/test', methods=['POST'])
def test():
	url = 'http://localhost:5000/v2/classify'
	headers = {'content-type': 'application/json'}
	request_json = request.json
	datasets = request_json['datasets']
	results = []
	for dataset in datasets:
		result = test_runner.runTest(url, headers, images, dataset)
		results.append(result)
	return {'results': results}

if __name__ == '__main__':
	app.run(port = 6000)