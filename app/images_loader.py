import os
from os.path import isdir, isfile, join
from image_serializer import *

def isNotHidden(x):
	return x[0] != '.'

def dirs(path):
	objects = os.listdir(path)
	return list(filter(isNotHidden, [x for x in objects if isdir(join(path, x))]))

def files(path):
	objects = os.listdir(path)
	return list(filter(isNotHidden, [x for x in objects if isfile(join(path, x))]))

def validAnswer(image, params):
	if params['dataset'] == None:
		return {
			'dataset': image['dataset'],
			'class': image['class'],
			'label': image['label']
		}
	else:
		return {
			'class': image['class'],
			'label': image['label']
		}

def loadImages(root_path='./images/'):
	images = {}
	datasets_names = dirs(root_path)

	for d_name in datasets_names:
		dataset_path = root_path + d_name + '/'
		images[d_name] = {}
		classes_numbers = dirs(dataset_path)
		labels = None
		with open(dataset_path + 'labels.json') as labels_file:
			labels = json.load(labels_file)

		for c_number in classes_numbers:
			class_path = dataset_path + c_number + '/'
			images[d_name][c_number] = []
			images_paths = [class_path + name for name in files(class_path)]
			serialized_images = serializeImages(images_paths)

			for i in range(len(images_paths)):
				images[d_name][c_number].append({
					'path': images_paths[i],
					'dataset': {
						'MNIST': 'MNIST',
						'FashionMNIST': 'Fashion MNIST'
					}[d_name],
					'class': int(c_number),
					'label': labels[int(c_number)],
					'data': serialized_images[i]
				})

	return images