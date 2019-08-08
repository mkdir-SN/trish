from ibm_watson import VisualRecognitionV3

import config
import json
import os


# Initialize VisualRecognition service with authentication details
vr = VisualRecognitionV3(
	version=config.vr_ver,
	iam_apikey=config.trish_apikey
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
			classifier_ids=config.classifier_ids).get_result()

	return details

def get_classes(details):
	classes = details["images"][0]["classifiers"][0]["classes"]

def get_waste_category(classes):
	if classes:
		return classes[0]["class"]
	return None

def identify_waste(img_file):
	details = get_details(img_file)
	classes = get_classes(details)
	waste_category = get_waste_category(classes)

	if waste_category is None:
		print("Visual Recognition could not sort the object into a waste category.")
		return

	# Possible edge cases: explicit content	

	# Send message back to user on Messenger 




