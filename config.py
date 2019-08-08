import os

DEBUG = True

# IBM auth details
TRISH_APIKEY = os.environ.get('trish_apikey')

CLASSIFIER_IDS = [
	os.environ.get('waste_classifier_id'),
	'explicit',
	]

VR_VER ='2018-03-19'

# FB auth details
FB_ACCESS_TOKEN = os.environ.get('fb_access_token')
FB_VERIFY_TOKEN = os.environ.get('fb_verify_token')