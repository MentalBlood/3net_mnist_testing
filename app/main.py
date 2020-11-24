import images_loader
images, amount_of_images = images_loader.loadImages()
print(len(images), 'datasets loaded', '(' + str(amount_of_images), 'images total)')

import test_runner
tests = test_runner.loadTests()
print(len(tests), 'tests loaded')

from reportGenerator import *

from flask import Flask, request
from flask_restful import Api, Resource
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

@app.route('/test', methods=['POST'])
def test():
	request_json = request.json

	baseUrl = request_json['url']
	headers = {'content-type': 'application/json'}
	
	tests_to_do = None
	if 'tests' in request_json:
		tests_to_do_names = request_json['tests']
		tests_to_do = [tests[name] for name in tests_to_do_names]
	else:
		tests_to_do = [tests[name] for name in tests]
	tests_results = [test_runner.runTest(baseUrl, headers, images, test) for test in tests_to_do]

	reportJSON = {
		'Total tests made': len(tests_results),
		'Passed': len(list(filter(lambda t: t['Test result'] == 'passed', tests_results))),
		'Failed': len(list(filter(lambda t: t['Test result'] == 'failed', tests_results))),
		'Results': tests_results
	}
	report = generateReport(reportJSON)
	
	return {'report': report}

if __name__ == '__main__':
	app.run()