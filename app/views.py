from app import app, vr
from app.messenger import Message, MessengerBot
from flask import Flask, request

import config
import json

messenger_bot = MessengerBot(config.FB_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if request.args.get("hub.verify_token") == config.FB_VERIFY_TOKEN:
			return request.args.get("hub.challenge"), 200
	return "Invalid verification token sent", 403

@app.route('/', methods=['POST'])
def handle():
	data = request.json

	m = Message(data)

	messenger_bot.process(m)

	return "Handled!"


