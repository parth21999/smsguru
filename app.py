#!/usr/bin/env python
 
# from urllib.parse import parse


import urllib.request
import urllib.parse
import json
from flask import Flask
from flask import request

# from flask import render_template

app = Flask(__name__)
apikey = 'A4mhT8jM+RY-ePSJWXB0P5pJuT5BzBBlVAumiqQiZJ'


def sendSMS(apikey, numbers, sender, message):
	data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
		'message' : message, 'sender': sender})
	data = data.encode('utf-8')
	request = urllib.request.Request("https://api.textlocal.in/send/?")
	f = urllib.request.urlopen(request, data)
	fr = f.read()
	return(fr)


@app.route('/', methods=["GET", "POST"])
def main_route():
	if request.method == "POST":
		number = request.form.get('sender')
		content = request.form.get('content')
		credits = request.form.get('credits')
		print("SENDER TYPE: " + type(number))
		print("CONTENT TYPE: " + type(content))
		print("CREDITS TYPE: " + type(credits))

		# if(credits > 0):
		# 	sendSMS(apikey, number, 'TXTLCL', content)

		print("MESSAGE CONTENT: " + request.form.get('content'))
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
