#!/usr/bin/env python
 
# from urllib.parse import parse


import urllib.request
import urllib.parse
import json
from flask import Flask
from flask import request

# from flask import render_template

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def main_route():
	if request.method == "POST":
		return request.form.get['content']
	else:
		return "hello world!!!"

@app.route('/messages', methods=["POST"])
def messages_route():
	content = request.form.get['content']

	return content

if __name__ == "__main__":
	app.run()





# def sendSMS(apikey, numbers, sender, message):
# 	data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
# 		'message' : message, 'sender': sender})
# 	data = data.encode('utf-8')
# 	request = urllib.request.Request("https://api.textlocal.in/send/?")
# 	f = urllib.request.urlopen(request, data)
# 	fr = f.read()
# 	return(fr)

# def getInboxes(apikey):
# 	data =  urllib.parse.urlencode({'apikey': apikey})
# 	data = data.encode('utf-8')
# 	request = urllib.request.Request("https://api.textlocal.in/get_inboxes/?")
# 	f = urllib.request.urlopen(request, data)
# 	fr = f.read()
# 	return(fr)

# def getMessages(apikey, inboxID):
# 	data =  urllib.parse.urlencode({'apikey': apikey, 'inbox_id' : inboxID})
# 	data = data.encode('utf-8')
# 	request = urllib.request.Request("https://api.textlocal.in/get_messages/?")
# 	f = urllib.request.urlopen(request, data)
# 	fr = f.read()
# 	return(fr)

# def stuff():
# 	apikey = 'A4mhT8jM+RY-ePSJWXB0P5pJuT5BzBBlVAumiqQiZJ'

# 	# resp =  sendSMS(apikey, '919205257278',
# 	#     'TXTLCL ', 'This is your message')

# 	# To get ID
# 	inboxes_bytes = getInboxes(apikey)
# 	inboxes = json.loads(inboxes_bytes.decode('utf8').replace("'", '"'))
# 	inbox_id = inboxes["inboxes"][0]["id"]
# 	# print (inbox_id)

# 	messages_bytes = getMessages(apikey, inbox_id)
# 	messages = json.loads(messages_bytes.decode('utf8').replace("'", '"'))

# 	print(messages)
# 	return
