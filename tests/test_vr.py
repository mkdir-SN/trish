from ibm_watson import VisualRecognitionV3
from app import vr

import config
import json
import unittest

path = "./test_vr_samples/"

def test_vr_apikey():
	assert config.TRISH_APIKEY is not None

def test_vr_waste_classifier_id():
	assert config.WASTE_CLASSIFER_ID is not None

vr = VisualRecognitionV3(
	version=config.VR_VER,
	iam_apikey=config.TRISH_APIKEY
)

def is_json(j):
	try:
		json_obj = json.loads(j)
	except ValueError as e:
		return False
	return True	

def test_get_details():
	human_details = vr.get_details(human)
	assert is_json(human_details) == True

def test_get_classifiers():
	pencil_details = vr.get_details(pencil)

