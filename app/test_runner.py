from random import shuffle
import requests
import json
from images_loader import validAnswer

def runTest(url, headers, images, dataset_name):
	request_json = {'dataset': dataset_name}

	images_for_test = []
	if dataset_name == None:
		for d_name in images:
			for c_number in images[d_name]:
				images_for_test += images[d_name][c_number]
	else:
		for class_number in images[dataset_name]:
			images_for_test += images[dataset_name][class_number]
	shuffle(images_for_test)
	data_for_test = [img['data'] for img in images_for_test]
	request_json['images'] = data_for_test

	answers_for_test = [validAnswer(img, request_json) for img in images_for_test]
	valid_response_json = {'predictions': answers_for_test}

	response = requests.post(url, json=request_json, headers=headers)
	response_json = json.loads(response.text)

	for i in range(len(response_json['predictions'])):
		got = response_json['predictions'][i]
		valid = valid_response_json['predictions'][i]
		if got != valid:
			print(got, '!=', valid)

	return response_json == valid_response_json