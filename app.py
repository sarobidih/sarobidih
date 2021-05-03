import random, json
from flask import Flask, request
from pymessenger.bot import Bot
import requests
from scrapping import scrapping_harenantsika_product
from response import help, other
from fbmessenger import BaseMessenger
from fbmessenger.elements import Text
from fbmessenger.attachments import Image, Video
import os
from requests_toolbelt import MultipartEncoder
import threading




app = Flask(__name__)
ACCESS_TOKEN = 'EAAC7aDEUsokBAJOGjZB5Q0p7hOx7ysvRjw2LPwWiU9Jc4GquZCV7wJntNJz9dmaE50cUipZBhlwZCbTcpuPRd2W4E7oUCGAEZBHsvQUJFUubbFi06zlzZBu7XQnaErpdFdwhzKrxPUj4u9733lVz1F5lpkEfTpAGAjZA8OKyeMbuAZDZD'
VERIFY_TOKEN = 'd8230120b243bf986a3f998a24db674c451160a6'
bot = Bot(ACCESS_TOKEN)

################ fb messenger #################"""
#test
def process_message(message):
	response = Video(url='https://brash-lime-enigmosaurus.glitch.me/myvideo.webm')
	return response.to_dict()


class Messenger(BaseMessenger):
	def __init__(self, page_access_token):
		self.page_access_token = page_access_token
		super(Messenger, self).__init__(self.page_access_token)

	def message(self, message):
		action = process_message(message)
		res = self.send(action, 'RESPONSE')
		return 'success'




request_check = {'previous': '', 'recent': ''}

messenger = Messenger(ACCESS_TOKEN)

POOL_TIME = 1000 #Seconds
dataLock = threading.Lock()
yourThread = threading.Thread()


# We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
	if request.method == 'GET':
		token_sent = request.args.get("hub.verify_token")
		return verify_fb_token(token_sent)
	else:
		output = request.get_json()
		for event in output['entry']:
			messaging = event['messaging']
			for message in messaging:
				if message.get('message'):
					recipient_id = message['sender']['id']
					if message['message'].get('text'):
						receive_message = message['message'].get('text').split()
						if (receive_message[0].upper() == "SEARCH"):
							if len(receive_message) < 2:
								send_message(recipient_id,'Veuillez réessayer la syntaxe exacte doit être search + produit_recherché')
							else:
								response_query = ' '.join(map(str, receive_message[1:]))
								send_message(recipient_id,'ok, recherche produit 🔑{}🔑 en cours ....'.format(response_query))
								results = scrapping_harenantsika_product(response_query)
								nbr_produit = len(results)
								if (nbr_produit == 0):
									send_message(recipient_id,'Désolé, votre recherche produit 🔑{}🔑 n\'éxiste pas'.format(response_query))
								else:
									send_generic_template_produit(recipient_id, response_query)

						elif (receive_message[0].upper() == "HELP"):
							response_sent_text = help()
							send_message(recipient_id, response_sent_text)
						else:
							response_sent_text = other()
							send_message(recipient_id, response_sent_text)


					if message['message'].get('attachments'):
						response_sent_nontext = get_message()
						send_message(recipient_id, response_sent_nontext)
	return 'success'







def timeout():
	return 'temps écouler'


def verify_fb_token(token_sent):
	if token_sent == VERIFY_TOKEN:
		return request.args.get("hub.challenge")
	return 'Invalid verification token'


def get_message():
	sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!",
						"We're greatful to know you :)"]
	return random.choice(sample_responses)


def send_message(recipient_id, response):
	bot.send_text_message(recipient_id, response)
	return "success"

def send_generic_template_produit(recipient_id, research_query):
	url = "https://graph.facebook.com/v9.0/me/messages?access_token=" + ACCESS_TOKEN
	results = scrapping_harenantsika_product(research_query)


	payload = []
	for result in results:
		title = result[0]
		price = result[1]
		desc = result[2]
		img = result[3]
		lien = result[4]
		payload.append({
			"title": "{} - Prix {}".format(title, price),
			"image_url": img,
			"subtitle": " Description :  {}".format(desc),
			"default_action": {
				"type": "web_url",
				"url": lien,
				"webview_height_ratio": "tall",
			},
			"buttons": [
				{
					"type": "web_url",
					"title": "Acheter",
					"url": "{}".format(lien)
				},
			]
		})
	extra_data = {
		"attachment": {
			"type": "template",
			"payload": {
				"template_type": "generic",
				"elements": payload
			}
		}
	}

	data = {
		'recipient': {'id': recipient_id},
		'message': {
			"attachment": extra_data["attachment"]
		}
	}
	resp = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
	postback_data = request.get_json()
	return "success"


def send_BM(recipient_id, response_sent_text, element):
	bot.send_button_message(recipient_id, response_sent_text, element)
	return "success"



if __name__ == "__main__":
	app.run()
