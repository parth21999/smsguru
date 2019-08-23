# nlp helper functions 
from App_files.nlp_helpers import (reduce_content, get_keywords, clean_content, 
check_spellings, summerize_content, clean_sms_content,
correct_case, detect_language)
# SMS helpers
from App_files.textlocal_helpers import sendSMS
# search helpers
from App_files.search_helpers import (search_duckduckgo, get_google_info, get_wiki_info)
# flask 
from flask import Flask
from flask import request
import os
# miscellanous
import json
import wikipedia
import pickle
from googletrans import Translator
# logging
import logging
import datetime
import json
application = app = Flask(__name__)
apikey = 'A4mhT8jM+RY-ePSJWXB0P5pJuT5BzBBlVAumiqQiZJ'
keyword = '7B3D9'

def get_info(sms_content):
	cleaned = clean_sms_content(sms_content)
	#cleaned = check_spellings(cleaned)
	query_lang = detect_language(sms_content)
	try:
		info = ''
		if query_lang == 'hi':
			info = get_google_info(cleaned)
		else:
			to_search = get_keywords(cleaned)
			print("search words:", to_search)
			info = search_duckduckgo(to_search)
			if (len(info) == 0):
				try:
					info = get_wiki_info(to_search)	
				except wikipedia.exceptions.PageError:
					info = get_google_info(to_search)
		if (len(info) != 0):
			return reduce_content(clean_content(info))
		else:
			return "No Information Found"
	except Exception as e:
		print(str(e))
		return "Error occured"

@app.route('/', methods=["GET", "POST"])
def main_route():
	if request.method == "POST":
		print("query received")
		sender_number = request.form.get('sender')
		content = request.form.get('content')
		credits = request.form.get('credits')
		info_to_send = get_info(content)
		print(info_to_send)
		if(int(credits) > 0):
			print("Sending response")
			send_resp = json.loads(sendSMS(sender_number, 'TXTLCL', info_to_send).decode('utf8').replace("'", '"'))
			print("Response: " + str(send_resp))
			cur_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
			query_info = f'{cur_datetime},{sender_number},{content},{info_to_send},{send_resp['status']}'
			app.logger.info(query_info)

		# print("MESSAGE CONTENT: " + request.form.get('content'))
	return "Hello world"

if __name__ == "__main__":
	handler = logging.FileHandler('usage_logs.csv')
	handler.setLevel(logging.INFO)
	f_format = logging.Formatter('%(message)s')
	handler.setFormatter(f_format)
	app.logger.addHandler(handler)
	app.run()
