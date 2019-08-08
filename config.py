import os

DEBUG = True

# IBM authentication details
trish_apikey = os.environ.get('trish_apikey')

classifier_ids = [
	os.environ.get('waste_classifier_id'),
	]

vr_ver='2018-03-19'

