#/usr/bin/env python

# nlp helper functions 
from nlp_helpers import (reduce_content, get_keywords, clean_content, 
check_spellings, summerize_content, clean_sms_content,
correct_case, detect_language)

from textlocal_helpers import sendSMS
# search helpers
from search_helpers import (search_duckduckgo, get_google_info, get_wiki_info)

from flask import Flask
from flask import request
import os

# miscellanous
import json
import wikipedia
import pickle
# for database integration
#import mysql.connector as mysql
from flaskext.mysql import MySQL
from googletrans import Translator

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'sql12300194'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jkhL9weFyW'
app.config['MYSQL_DATABASE_DB'] = 'sql12300194'
app.config['MYSQL_DATABASE_HOST'] = 'sql12.freemysqlhosting.net'


mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

apikey = 'A4mhT8jM+RY-ePSJWXB0P5pJuT5BzBBlVAumiqQiZJ'
keyword = '7B3D9'

def update_database(phoneNumber, query):
	# Checking if number exists in database
	print("updating DB")
	search_results = cursor.execute("SELECT * FROM users WHERE PhoneNumber = (%s)", phoneNumber)
	if len(search_results) == 0:
		SQL_formula = "INSERT INTO users (PhoneNumber) VALUES (%s)"
		cursor.execute(SQL_formula, phoneNumber)
	conn.commit()

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
		update_database(sender_number, content)
		credits = request.form.get('credits')
		info_to_send = get_info(content)
		print(content)
		if(int(credits) > 0):
			send_resp = sendSMS(sender_number, 'TXTLCL', info_to_send).decode('utf8').replace("'", '"')
			print("Response: " + send_resp)

		# print("MESSAGE CONTENT: " + request.form.get('content'))
	return "Hello world"

if __name__ == "__main__":
	app.run()
