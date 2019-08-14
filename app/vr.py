from app.messenger import Message
from ibm_watson import VisualRecognitionV3

import config
import json
import os

# Initialize VisualRecognition service with authentication details
vr = VisualRecognitionV3(
	version=config.VR_VER,
	iam_apikey=config.TRISH_APIKEY
)

waste_types = {
	"recyclable": "Recyclable",
	"landfill": "Landfill",
	"compost": "Compost",
	"hazardous_waste": "Hazardous waste"
}

valid_files = (
	'.gif',
	'.jpg',
	'.jpeg',
	'.png',
	'.tif'
)

valid_files_str = ''

for f in valid_files:
	valid_files_str += f + ' '

def identify_waste(img_url):
	"""
	Identifies waste and sends a corresponding message to user.
	"""
	details = get_details(img_url)
	classifiers = get_classifiers(details)
	print(json.dumps(classifiers, indent=2))

	if is_explicit(classifiers):
		return "explicit"

	waste_type = get_waste_type(classifiers)

	if waste_type is None:
		return None

	return waste_types[waste_type]

def get_details_img_file(img_file):
	"""
	Obtain results of classification query to IBM Visual Recognition custom waste model using img file. 
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

def get_details(img_url):
	"""
	Obtain results of classification query to IBM Visual Recognition custom waste model using img url. 
	The model is specified by classifier_id.

	img_url has the correct protocol because img_url is provided by Messenger's POST request under attachments.
	"""

	details = vr.classify(
		url=img_url,
		threshold='0.7',
		classifier_ids=config.CLASSIFIER_IDS).get_result()

	return details

def get_classifiers(details):
	return details["images"][0]["classifiers"]

def get_waste_type(classifiers):
	waste_classes = None
	for c in classifiers:
		if c["classifier_id"] == config.WASTE_CLASSIFIER_ID:
			waste_classes = c["classes"]
			break

	if waste_classes:
		return waste_classes[0]["class"]

	return

def is_explicit(classifiers):
	explicit_classes = None

	for c in classifiers:
		if c["classifier_id"] == "explicit":
			explicit_classes = c["classes"]
			break

	if explicit_classes:
		explicity = explicit_classes[0]["class"]
		if explicity == "not explicit":
			return False
		elif explicity == "explicit":
			return True
	else:
		return None






