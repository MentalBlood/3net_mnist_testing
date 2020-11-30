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
		'Test name': test['name'],
		'Test result': 'passed',
		'Requests': []
	}
	for request in test['requests']:
		requestUrl = baseUrl + request['destination']['api_version'] \
		                     + '/' + request['destination']['resource']
		request_report = {
			'Request URL': requestUrl,
			'Request results': []
		}
		amount = request['amount']
		for i in range(amount):
			result = makeRequest(requestUrl, headers, images, request['images'])
			if result['Is response valid'] == 'no':
				if len(list(filter(lambda e: e['Error type'].startswith('microservice error:'), result['Errors']))):
					test_report['Test result'] = 'failed'
			request_report['Request results'].append(result)

		test_report['Requests'].append(request_report)

	return test_report