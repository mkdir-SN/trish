from app import vr

import config

class Message:

	def __init__(self, data):
		self.data = data

	def get_img_urls(self):
		img_urls = []
		attachments = self.get_attachments()
		for attachment in attachments:
			if attachment["type"] == "image":
				img_urls.append(attachment["payload"]["url"])
		return img_urls

	def get_sender_id(self):
		return self.data["entry"][0]["messaging"][0]["sender"]["id"]

	def get_recipient_id(self):
		return self.data["entry"][0]["messaging"][0]["recipient"]["id"]

	def get_attachments(self):
		return self.data["entry"][0]["messaging"][0]["message"]["attachments"]

def reply(message):
	
