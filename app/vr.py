from ibm_watson import VisualRecognitionV3

import config
import json
import os

# Initialize VisualRecognition service with authentication details
vr = VisualRecognitionV3(
	version=config.VR_VER,
	iam_apikey=config.TRISH_APIKEY
)

valid_files = (
	'.gif',
	'.jpg',
	'.png',
	'.tif'
)

valid_files_str = ''

for f in valid_files:
	valid_files_str += f + ' '

def identify_waste(img_file):
	"""
	Identifies waste and sends a corresponding message to user.
	"""
	details = get_details(img_file)
	classifiers = get_classifiers(details)
	print(json.dumps(classifiers, indent=2))

	if is_explicit(classifiers):
		print("Please refrain from sending explicit images to Trish.")
		return

	waste_type = get_waste_type(classifiers)

	if waste_type is None:
		print("Visual Recognition could not sort the object into a waste category.")
		return

	print("The object in the image is " + waste_type + ".")

def get_details(img_file):
	"""
	Obtain results of classification query to IBM Visual Recognition custom waste model. 
	The model is specified by classifier_id.
	"""

	if os.path.splitext(img_file)[-1] not in valid_files:
		raise TypeError("Image file is not one of the following file types: " + valid_files_str)
	
	with open(img_file, 'rb') as img_file:
		details = vr.classify(
			images_file=img_file,
			threshold='0.7',
			classifier_ids=config.CLASSIFIER_IDS).get_result()

	return details

def get_classifiers(details):
	return details["images"][0]["classifiers"]

def get_waste_type(classifiers):
	waste_classes = classifiers[0]["classes"]

	if waste_classes:
		return waste_classes[0]["class"]
	return None

def is_explicit(classifiers):
	explicit_classes = classifiers[1]["classes"]

	if explicit_classes:
		explicity = explicit_classes[0]["class"]
		print(explicity)
		if explicity is "not explicit":
			return False
		elif explicity is "explicit":
			return True
	else:
		print("Visual Recognition could not identify explicity of image.")
		return None






