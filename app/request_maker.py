import requests
import json
from random import shuffle, sample
from images_loader import validAnswer

def getImagesForRequest(images, params):
	images_for_test = []

	if not ('dataset' in params):
		for dataset_name in images:
			for class_number in images[dataset_name]:
				images_for_test += images[dataset_name][class_number]
	else:
		dataset_name = params['dataset']['name']
		if not ('classes' in params['dataset']):
			for class_number in images[dataset_name]:
				images_for_test += images[dataset_name][class_number]
		else:
			for class_number in params['dataset']['classes']:
				new_images = images[dataset_name][class_number]
				new_max_amount = params['dataset']['classes'][class_number]['amount']
				images_for_test += sample(new_images, new_max_amount) if (new_max_amount >= 0 and new_max_amount < len(new_images)) else new_images

	max_amount = params['amount']
	images_for_test = sample(images_for_test, max_amount) if (max_amount >= 0 and max_amount < len(images_for_test)) else images_for_test

	return images_for_test

def makeRequest(url, headers, images, params):
	request_json = {}
	if 'dataset' in params:
		request_json['dataset'] = params['dataset']['name']

	images_for_test = getImagesForRequest(images, params)
	shuffle(images_for_test)
	data_for_test = [img['data'] for img in images_for_test]
	request_json['images'] = data_for_test

	answers_for_test = [validAnswer(img, request_json) for img in images_for_test]
	valid_response_json = {'predictions': answers_for_test}

	response = requests.post(url, json=request_json, headers=headers)
	response_json = json.loads(response.text)

	test_passed = response_json == valid_response_json
	if test_passed:
		return {'Is response valid': 'yes'}
	else:
		errors = []
		if not ('predictions' in response_json):
			errors.append({
				'Error type': 'microservice error: invalid response JSON structure',
				'Error description': 'absence_of_predictions_field'
			})
		else:
			for i in range(len(response_json['predictions'])):
				got = response_json['predictions'][i]
				valid = valid_response_json['predictions'][i]
				if got != valid:
					errors.append({
						'Error type': 'model error: incorrect prediction',
						'Error description': {
							'image path': images_for_test[i]['path'],
							'valid answer': valid,
							'got answer': got
						}
					})
		if len(errors) == 0:
			errors.append({
				'Error type': 'microservice error: invalid response JSON structure',
				'Error description': {
					'valid json': valid_response_json,
					'got json': response_json
				}
			})
		return {'Is response valid': 'no', 'Errors': errors}