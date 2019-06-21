#!/usr/bin/env python
# Deploying
# from urllib.parse import parse
import urllib.request
import urllib.parse
import json
import wikipedia
import re
from flask import Flask
from flask import request
from googletrans import Translator
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import os
from duckduckpy import query
# For selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Setting up for google query
chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
chrome_options = Options()
chrome_options.binary_location =chrome_bin
chrome_options.add_argument("--window-size=1024x768")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path = "chromedriver", chrome_options=chrome_options)



app = Flask(__name__)
apikey = 'A4mhT8jM+RY-ePSJWXB0P5pJuT5BzBBlVAumiqQiZJ'
keyword = '7B3D9'

# st = StanfordNERTagger(model_filename=modelfile, path_to_jar=jarfile)


def get_named_entity(text):
	chunked = ne_chunk(pos_tag(word_tokenize(text)))
	prev = None
	continuous_chunk = []
	current_chunk = []
	for i in chunked:
		if type(i) == Tree:
			current_chunk.append(" ".join([token for token, pos in i.leaves()]))
		elif current_chunk:
			named_entity = " ".join(current_chunk)
			if named_entity not in continuous_chunk:
				continuous_chunk.append(named_entity)
				current_chunk = []
			else:
				continue
	return continuous_chunk

def sendSMS(numbers, sender, message):
	data =  urllib.parse.urlencode({'username': 'parth21999@gmail.com', 'password': 'Partharjun1',
		'numbers': numbers, 'message' : message, 'sender': sender, 'unicode':'true'})
	data = data.encode('utf-8')
	request = urllib.request.Request("https://api.textlocal.in/send/?")
	f = urllib.request.urlopen(request, data)
	fr = f.read()
	return(fr)

def remove_parentheses(content):
	clean_content = re.sub(r'\([^)]*\)', '', content)
	clean_content = re.sub(r'\[[^)]*\]', '', clean_content)
	return clean_content

def shrink_content(content):
	if len(content) <= 160:
		return content

	char_limit = 160
	# last_period = content[:char_limit].rfind('.')
	last_purna_viram = content[:char_limit].rfind('\u0964')

	if (last_purna_viram == -1):
		last_purna_viram = char_limit - 1

	return content[:last_purna_viram + 1]

def search_duckduckgo(search_word):
	response = query(search_word, container="dict")['abstract']
	return response

def search_wikipedia(search_word):
	top_result = wikipedia.search(search_word)[0]
	content = wikipedia.page(top_result).content
	return content

def search_hindi_wikipedia(search_word):
	wikipedia.set_lang('hi')
	search_word_hindi = translate_to_hindi(search_word)
	content = wikipedia.summary(search_word_hindi, chars=600, auto_suggest=False)
	return content

def clean_sms_content(sms_content):
	sms_content = sms_content.replace(keyword, '')
	sms_content = sms_content.strip()
	return sms_content

def translate_to_hindi(info):
	translator = Translator()
	info_in_hindi = translator.translate(info, dest='hindi')
	return info_in_hindi.text

def translate_to_english(info):
	translator = Translator()
	info_in_english = translator.translate(info, dest='english')
	return info_in_english.text

def ask_google(query):
	query = query.replace(' ', '+')
	driver.get('http://www.google.com/search?q=' + query)
	answer = driver.execute_script( "return document.elementFromPoint(arguments[0], arguments[1]);", 350, 230).text
	return answer



def get_info(sms_content):
	cleaned = clean_sms_content(sms_content)
	to_search_english = translate_to_english(cleaned)
	info = search_duckduckgo(to_search_english)
	if not info:
		print("ask_google: " + ask_google(to_search_english))
		info = ask_google(to_search_english)

		if not info:
			try:
				to_search_english = to_search_english + ' .'
				print('to_search_english: ' + to_search_english)
				to_search = get_named_entity(to_search_english)[0]
			except:
				to_search = to_search_english

			print('to_search: ' + to_search)

			try:
				info_in_hindi = search_hindi_wikipedia(to_search)
			except wikipedia.exceptions.PageError:
				try:
					info = search_wikipedia(to_search)
				except wikipedia.exceptions.PageError:
					info = "No answer found"

	info_in_hindi = translate_to_hindi(info)
	# print("Before shrinking: " + info_in_hindi)
	info_in_hindi = remove_parentheses(shrink_content(info_in_hindi))
	# print("After shrinking: " + info_in_hindi)
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
