import json
import base64

def serializeImages(images_paths_list):
	def readImage(path):
		result = None
		with open(path, 'rb') as image:
			imageBytes = open(path, 'rb').read()
			result = base64.encodebytes(imageBytes).decode("utf-8")
		return result
	serializedImages = list(map(readImage, images_paths_list))
	return serializedImages