#!/usr/bin/env python
 
# from urllib.parse import parse

import urllib.request
import urllib.parse
import json
import wikipedia
from flask import Flask
from flask import request
from googletrans import Translator
import HTMLParser


app = Flask(__name__)
apikey = 'A4mhT8jM+RY-ePSJWXB0P5pJuT5BzBBlVAumiqQiZJ'
keyword = '7B3D9'



def sendSMS(numbers, sender, message):
	data =  urllib.parse.urlencode({'username': 'parth21999@gmail.com', 'password': 'Partharjun1', 'numbers': numbers,
		'message' : message, 'sender': sender, 'unicode' : 'True'})
	data = data.encode('utf-8')
	request = urllib.request.Request("https://api.textlocal.in/send/?")
	f = urllib.request.urlopen(request, data)
	fr = f.read()
	return(fr)

def shrink_content(content):
	char_limit = 160
	last_period = content[:char_limit].rfind('.')
	return content[:last_period + 1]

def search_wikipedia(search_word):
	top_result = wikipedia.search(search_word)[0]
	content = wikipedia.page(top_result).content
	content = shrink_content(content)
	return content

def clean_sms_content(sms_content):
	sms_content = sms_content.replace(keyword, '')
	sms_content = sms_content.strip()
	return sms_content

def translate(info):
	translator = Translator()
	info_in_hindi = translator.translate(info, dest='hindi')
	return info_in_hindi

class parseTitle(HTMLParser.HTMLParser):

	def handle_starttag(self, tag, attrs):
		if tag == 'Translated':
			print("ENTERED FUNCTION")
			for names, values in attrs:
				if name == 'text':
					return value 
				
	
def get_info(sms_content):
	to_search = clean_sms_content(sms_content)
	info = search_wikipedia(to_search)
	info_in_hindi = translate(info)
	aparser = parseTitle() 
	info_in_hindi = aparser.feed(info_in_hindi.read())
	print(info_in_hindi)
	return info_in_hindi







@app.route('/', methods=["GET", "POST"])
def main_route():
	if request.method == "POST":
		sender_number = request.form.get('sender')
		content = request.form.get('content')
		credits = request.form.get('credits')

		info_to_send = get_info(content)

		# print(sender_number)

		if(int(credits) > 0):
			send_resp = sendSMS(sender_number, 'TXTLCL', info_to_send).decode('utf8').replace("'", '"')
			print("Response: " + send_resp)

		# print("MESSAGE CONTENT: " + request.form.get('content'))
	return "hello world!!!"

if __name__ == "__main__":
	app.run()






# def getInboxes(apikey):
# 	data =  urllib.parse.urlencode({'apikey': apikey})
# 	data = data.encode('utf-8')
# 	request = urllib.request.Request("https://api.textlocal.in/get_inboxes/?")
# 	f = urllib.request.urlopen(request, data)
# 	fr = f.read()
# 	return(fr)
# def stuff():

# 	# resp =  sendSMS(apikey, '919205257278',
# 	#     'TXTLCL ', 'This is your message')




# 	messages_bytes = getMessages(apikey, inbox_id)
# 	messages = json.loads(messages_bytes.decode('utf8').replace("'", '"'))

# 	print(messages)
# 	return
# reruning app