import os

DEBUG = True

# IBM auth details
TRISH_APIKEY = os.environ.get('trish_apikey')

WASTE_CLASSIFIER_ID = os.environ.get('waste_classifier_id')

CLASSIFIER_IDS = [
	WASTE_CLASSIFIER_ID,
	'explicit',
	]

VR_VER ='2018-03-19'

# FB auth details
FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')