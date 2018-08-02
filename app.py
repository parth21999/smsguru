#!/usr/bin/env python
 
# from urllib.parse import parse


import urllib.request
import urllib.parse
import json
import wikipedia
from flask import Flask
from flask import request

# from flask import render_template

app = Flask(__name__)
apikey = 'A4mhT8jM+RY-ePSJWXB0P5pJuT5BzBBlVAumiqQiZJ'


def sendSMS(numbers, sender, message):
	data =  urllib.parse.urlencode({'username': 'parth21999@gmail.com', 'password': 'Partharjun1', 'numbers': numbers,
		'message' : message, 'sender': sender})
	data = data.encode('utf-8')
	request = urllib.request.Request("https://api.textlocal.in/send/?")
	f = urllib.request.urlopen(request, data)
	fr = f.read()
	return(fr)

def search_wikipedia(search_word):
	top_result = wikipedia.search(search_word)[0]
	content = wikipedia.page(top_result).content[:160]
	print(type(content))
	return content




@app.route('/', methods=["GET", "POST"])
def main_route():
	if request.method == "POST":
		sender_number = request.form.get('sender')
		content = request.form.get('content')
		credits = request.form.get('credits')

		print(sender_number)

		if(int(credits) > 0):
			send_resp = sendSMS(sender_number, 'TXTLCL', content).decode('utf8').replace("'", '"')
			print("Response: " + send_resp)

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
