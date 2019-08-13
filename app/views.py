from app import app, messenger, vr
from flask import Flask, request

import config
import json

@app.route('/', methods=['GET'])
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if request.args.get("hub.verify_token") == config.FB_VERIFY_TOKEN:
			return request.args.get("hub.challenge"), 200
	return "Invalid verification token sent", 403

@app.route('/', methods=['POST'])
def handle():
	data = request.json
	print(json.dumps(data, indent=2))

	return "Handled!"

