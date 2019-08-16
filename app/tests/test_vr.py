from app import vr

import config
import json
import pytest
import unittest

# Images from each waste category for testing
human = "https://raw.githubusercontent.com/mkdir-SN/trish/master/tests/test_vr_samples/human.jpg"
luminescent_bulb = "https://raw.githubusercontent.com/mkdir-SN/trish/master/tests/test_vr_samples/luminescent_bulb.jpg"
paper_cup = "https://raw.githubusercontent.com/mkdir-SN/trish/master/tests/test_vr_samples/paper_cup.jpg"
pencil = "https://raw.githubusercontent.com/mkdir-SN/trish/master/tests/test_vr_samples/pencil.jpg"
plastic_bottle = "https://raw.githubusercontent.com/mkdir-SN/trish/master/tests/test_vr_samples/plastic_bottle.jpg"

def test_vr_apikey():
	assert config.TRISH_APIKEY is not None

def test_vr_waste_classifier_id():
	assert config.WASTE_CLASSIFIER_ID is not None

def test_get_classifiers():
	pencil_details = vr.get_details(pencil)
	pencil_classifiers = vr.get_classifiers(pencil_details)
	first_classifier = pencil_classifiers[0]
	assert ('classifier_id' in first_classifier) == True

def test_get_waste_type():
	paper_cup_details = vr.get_details(paper_cup)
	paper_cup_classifiers = vr.get_classifiers(paper_cup_details)
	assert vr.get_waste_type(paper_cup_classifiers) == "recyclable"

def test_is_explicit():
	luminescent_bulb_details = vr.get_details(luminescent_bulb)
	luminescent_bulb_classifiers = vr.get_classifiers(luminescent_bulb_details)
	assert vr.is_explicit(luminescent_bulb_classifiers) is False

def test_identify_waste_plastic_bottle():
	assert vr.identify_waste(plastic_bottle) == "Recyclable"

def test_identify_waste_pencil():
	assert vr.identify_waste(pencil) == "Hazardous waste"

def test_identify_waste_human():
	assert vr.identify_waste(human) is None
