import os
from os.path import isdir, isfile, join

def isNotHidden(x):
	return x[0] != '.'

def dirs(path):
	objects = os.listdir(path)
	return list(filter(isNotHidden, [x for x in objects if isdir(join(path, x))]))

def files(path):
	objects = os.listdir(path)
	return list(filter(isNotHidden, [x for x in objects if isfile(join(path, x))]))

def validAnswer(image, params):
	if not ('dataset' in params):
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