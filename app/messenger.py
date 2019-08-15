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
				if self.is_sticker(payload):
					img_urls.append("sticker")
				else:
					img_urls.append(payload["url"])
			else:
				img_urls.append(None)
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
			self.send(uid, "Sorry, I currently can't handle text-based messages. Please send me images instead!")
		else:
			img_urls = message.get_img_urls()
			photo_no = 1 

			if len(img_urls) > 1:
				self.send(uid, "The numbering of the photos is from left to right, top to bottom.")

			for img_url in img_urls:

				# To avoid using VR API for stickers or unknown filetypes (.pdf, .zip, etc.)
				if img_url == "sticker":
					self.send(uid, "Sorry, but I can't sort stickers into waste categories, as cute as they are!")
					continue
				elif img_url is None:
					self.send(uid, "Sorry, I don't have the ability to process the type of message you just sent me. Consider sending me images instead!")
					continue 

				waste_category = vr.identify_waste(img_url)

				if waste_category:
					if waste_category == "explicit":
						self.send(uid, "Please don't send explicit material(s) to me. Thanks!")
						break
					self.send(uid, '{0} in photo {1}.'.format(waste_category, str(photo_no)))
				else:
					self.send(uid, "Sorry, I couldn't sort the object in photo {0} into a waste category.".format(str(photo_no)))

				# To keep track of the photo number for user readability 
				photo_no += 1

	def send(self, uid, body):

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



