import json
from common import *
from request_maker import *

def loadTests(path = './tests/'):
	tests = {}

	tests_paths = [path + name for name in files(path)]
	for test_path in tests_paths:
		with open(test_path) as test_file:
			test = json.load(test_file)
			tests[test['name']] = test

	return tests

def runTest(baseUrl, headers, images, test):
	test_report = {
		'name': test['name'],
		'requests': [],
		'verdict': 'passed',
	}
	for request in test['requests']:
		requestUrl = baseUrl + request['destination']['api_version'] \
		                     + '/' + request['destination']['resource']
		request_report = {
			'url': requestUrl,
			'results': []
		}
		amount = request['amount']
		for i in range(amount):
			result = makeRequest(requestUrl, headers, images, request['images'])
			if result['valid'] == False:
				test_report['verdict'] = 'failed'
			request_report['results'].append(result)

		test_report['requests'].append(request_report)

	return test_report