import os
import json
import requests
from image_serializer import serializeImages

def loadImagesAndAnswers(dataset_name, root_path = './images/'):
	images = []
	answers = []

	dataset_path = root_path + dataset_name + '/'

	labels_path = dataset_path + 'labels.json'
	labels = None
	with open(labels_path) as labels_file:
		 labels = json.load(labels_file)

	images_paths = []
	classes_numbers = os.listdir(dataset_path)
	for class_number in classes_numbers:
		class_path = dataset_path + class_number + '/'
		if not os.path.isdir(class_path):
			continue
		
		images_names = os.listdir(class_path)
		images_paths += list(map(lambda name: class_path + name, images_names))
		
		current_class_correct_answers = [{
			'class': int(class_number),
			'label': labels[int(class_number)]
		}] * len(images_names)
		answers += current_class_correct_answers

	images = serializeImages(images_paths)
	answer = {'predictions': answers }

	return {
		'images': images,
		'answer': answer,
		'images_paths': images_paths
	}

def sendAndVerifyAnswer(url, headers, data, net_name, correct_answer, additional_info):
	request_json = {'images': data, 'dataset': net_name}
	response = requests.post(url, json=request_json, headers=headers)
	response_json = response.json()
	incorrect_answers_reports = []
	for i in range(len(response_json['predictions'])):
		if response_json['predictions'][i] != correct_answer['predictions'][i]:
			incorrect_answers_reports.append(additional_info[i] + ': ' + str(response_json['predictions'][i]) + ' != ' + str(correct_answer['predictions'][i]))
	print(net_name + ':')
	if len(incorrect_answers_reports) != 0:
		print('FAILED:')
		for report in incorrect_answers_reports:
			print(report)
	else:
		print('OK')
	return response_json == correct_answer

def runSampleTest(dataset_name):
	url = 'http://localhost:5000/v1/classify'
	headers = {'content-type': 'application/json'}
	loaded = loadImagesAndAnswers(dataset_name)
	result = sendAndVerifyAnswer(url, headers, loaded['images'], dataset_name, loaded['answer'], loaded['images_paths'])
	return result