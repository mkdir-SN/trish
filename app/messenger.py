from app import vr

import config
import json
import requests

class Message:

	def __init__(self, data):
		self.data = data

	def get_img_urls(self):
		img_urls = []
		attachments = self.get_attachments()
		for attachment in attachments:
			if attachment["type"] == "image":
				payload = attachment["payload"]
				if not self.is_sticker(payload):
					img_urls.append(payload["url"])
		return img_urls

	def is_text(self):
		if self.data["entry"][0]["messaging"][0]["message"].get("text"):
			return True
		return False

	def is_sticker(self, payload):
		"""
		Uses payload to determine if attachments contains a sticker, rather than assuming attachment will be one sticker (to account for possible changes in Facebook updates).
		"""
		if payload.get("sticker_id"):
			return True
		return False

	def get_sender_id(self):
		return self.data["entry"][0]["messaging"][0]["sender"]["id"]

	def get_recipient_id(self):
		return self.data["entry"][0]["messaging"][0]["recipient"]["id"]

	def get_attachments(self):
		return self.data["entry"][0]["messaging"][0]["message"]["attachments"]

class MessengerBot:

	def __init__(self, access_token):
		self.ACCESS_TOKEN = access_token

	def process(self, message):
		uid = message.get_sender_id()

		typing = {
			"recipient": { "id": uid },
			"sender_action": "typing_on"
		}

		self.response(typing)

		if message.is_text():
			self.reply(uid, "Trish currently cannot handle text-type messages. Please send images instead!")
		else:
			img_urls = message.get_img_urls()
			photo_no = 1

			for img_url in img_urls:

				waste_category = vr.identify_waste(img_url)

				if waste_category:
					if waste_category == "explicit":
						self.reply(uid, "Please do not send explicit material to Trish.")
						break
					self.reply(uid, waste_category + ' in photo ' + str(photo_no) + '.')
				else:
					self.reply(uid, "Trish could not sort the object in photo " + str(photo_no) + " into a waste category.")

				photo_no += 1

	def reply(self, uid, body):

		# Display typing by sending a separate request
		msg = {
			"messaging_type": "response",
			"recipient": { "id": uid },
			"message": { "text": body }
			}

		self.response(msg)

	def response(self, data):
		r = requests.post("https://graph.facebook.com/v4.0/me/messages",
		params={"access_token": self.ACCESS_TOKEN},
		headers={"Content-Type": "application/json"},
		data=json.dumps(data))



