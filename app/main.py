import images_loader
images, amount_of_images = images_loader.loadImages()
print(len(images), 'datasets loaded', '(' + str(amount_of_images), 'images total)')

import test_runner
tests = test_runner.loadTests()
print(len(tests), 'tests loaded')

from flask import Flask, request
from flask_restful import Api, Resource
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

@app.route('/test', methods=['POST'])
def test():
	baseUrl = 'http://localhost:5000/'
	headers = {'content-type': 'application/json'}
	
	request_json = request.json
	
	tests_to_do_names = request_json['tests']
	tests_to_do = [tests[name] for name in tests_to_do_names]
	tests_results = [test_runner.runTest(baseUrl, headers, images, test) for test in tests_to_do]

	return {
		'total': len(tests_results),
		'passed': len(list(filter(lambda t: t['verdict'] == 'passed', tests_results))),
		'failed': len(list(filter(lambda t: t['verdict'] == 'failed', tests_results))),
		'tests_results': tests_results
	}

if __name__ == '__main__':
	app.run(port = 6000)