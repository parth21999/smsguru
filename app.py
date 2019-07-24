#/usr/bin/env python
# Deploying again
# from urllib.parse import parse
import urllib.request
import urllib.parse
import json
import wikipedia
import re
from flask import Flask
from flask import request
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import os
from duckduckpy import query
# keyword extraction
from rake_nltk import Rake
# for meaningCloud
import requests
# for google search urls
from googlesearch import search
# for case correction
import truecase
# for database integration
import mysql.connector as mysql

app = Flask(__name__)
apikey = 'A4mhT8jM+RY-ePSJWXB0P5pJuT5BzBBlVAumiqQiZJ'
keyword = '7B3D9'

def updateDatabase(phoneNumber, query):
	# connector setup
	my_db = mysql.connect(
		host="localhost",
		user="root",
		password="partharjun2002",
		database="SMSGuru"
	)
	my_cursor = my_db.cursor()
	# Checking if number exists in database
	search_results = my_cursor.execute("SELECT * FROM Users WHERE PhoneNumber = (%s)", (phoneNumber,))
	if len(search_results) == 0:
		SQL_formula = "INSERT INTO Users (PhoneNumber) VALUES (%s)"
		my_cursor.execute(SQL_formula, (phoneNumber,))

def reduce_content(content):
	punctuations = [".", ",", "!", "?", ":", ";"]
	last_space = 0
	space_found = False
	max_length = len(content) - 1
	if (len(content) > 150):
		max_length = 150
	for i in range(max_length, max_length - 20, -1):
		if content[i] == " " and not space_found:
			space_found = True
			last_space = i
		if content[i] in punctuations:
			return content[:(i+1)]
	return content[:last_space]

def get_named_entity(text):
    try:
        words = word_tokenize(text)
        tagged = pos_tag(words)
        named_ent_tree = ne_chunk(tagged, binary=True)
        named_ents = []
        for node in named_ent_tree:
            if type(node) is Tree and node.label() == "NE":
                named_ents.append(" ".join([n[0] for n in node.leaves()]))
        return named_ents
    except Exception as e:
        print(str(e))

def get_keywords(text):
	r = Rake()
	r.extract_keywords_from_text(text)
	return " ".join(r.get_ranked_phrases())

def sendSMS(numbers, sender, message):
	data =  urllib.parse.urlencode({'username': 'parth21999@gmail.com', 'password': 'Partharjun1',
		'numbers': numbers, 'message' : message, 'sender': sender, 'unicode':'true'})
	data = data.encode('utf-8')
	request = urllib.request.Request("https://api.textlocal.in/send/?")
	f = urllib.request.urlopen(request, data)
	fr = f.read()
	return(fr)

def clean_content(content):
	# removing bracket content
	clean_content = re.sub(r'\([^)]*\)', '', content)
	clean_content = re.sub(r'\[[^)]*\]', '', clean_content)
	# removing urls 
	clean_content = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', clean_content, flags=re.MULTILINE)
	return clean_content

def get_end_index(text, fl_index):
    i = fl_index
    while (i < len(text) - 1):
        i += 1
        if (text[i] == " "):
            break
    if (i == len(text) -1):
        return i + 1
    else:
        return i

def check_spellings(text):
	case_corrected = truecase.get_true_case(text)
	named_entities = get_named_entity(text)
	ne_indexes = []
	print(named_entities)
	for ne in named_entities:
		for match in re.finditer(ne, text):
			ne_indexes.append(match.start())
	url = "http://api.grammarbot.io/v2/check"
	corrections = []
	params = [('api_key', 'AF5B9M2X'), ('text', case_corrected), ('language', 'en-US')]
	responses = requests.get(url, params=params).json()['matches']
	for rspn in responses:
		corrections.append((rspn['replacements'][0]['value'], rspn['offset']))
	print(corrections)
	print(ne_indexes)

def summerize_content(search_url, sentences=1):
	url = "https://api.meaningcloud.com/summarization-1.0"
	payload = "key=4b942c0c5d7c9c76c99ba727d2df9b66&sentences=2&url=" + search_url
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	response = requests.request("POST", url, data=payload, headers=headers)
	return response.text

def search_duckduckgo(search_word):
	response = query(search_word, container="dict")['abstract']
	return response

def get_wikipedia_page(search_word):
	top_result = wikipedia.page(search_word)
	print(top_result.url)
	return top_result.url

def clean_sms_content(sms_content):
	sms_content = sms_content.replace(keyword, '')
	sms_content = sms_content.strip()
	return sms_content

def correct_case(text):
	return truecase.get_true_case(text)

def get_google_results(search_word):
	results = []
	# removing youtube urls
	for result in search(search_word, stop=10):
		print(result)
		if not re.match(r"https://www.youtube", result):
			results.append(result)
	return results 

def get_info(sms_content):
	cleaned = clean_sms_content(sms_content)
	#cleaned = check_spellings(cleaned)
	to_search = get_keywords(cleaned)
	print("search words:", to_search)
	info = search_duckduckgo(to_search)
	if (len(info) == 0):
		try:
			wiki_page = get_wikipedia_page(to_search)
			info = json.loads(summerize_content(wiki_page))['summary']
		except wikipedia.exceptions.PageError:
			for result in get_google_results(to_search):
				info = json.loads(summerize_content(result, 3))['summary']
				if (len(info) != 0):
					info_found = True
					break
	if (len(info) != 0):
		return reduce_content(clean_content(info))
	else:
		return "No Information Found"

@app.route('/', methods=["GET", "POST"])
def main_route():
	if request.method == "POST":
		sender_number = request.form.get('sender')
		content = request.form.get('content')
		updateDatabase(sender_number, content)
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
