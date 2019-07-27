import re
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from rake_nltk import Rake
import truecase
from googletrans import Translator
import requests

keyword = '7B3D9'

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

def clean_content(content):
	# removing bracket content
	clean_content = re.sub(r'\([^)]*\)', '', content)
	clean_content = re.sub(r'\[[^)]*\]', '', clean_content)
	# removing urls 
	clean_content = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', clean_content, flags=re.MULTILINE)
	return clean_content

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

def clean_sms_content(sms_content):
	sms_content = sms_content.replace(keyword, '')
	sms_content = sms_content.strip()
	return sms_content

def correct_case(text):
	return truecase.get_true_case(text)

def detect_language(text):
	translator = Translator()
	lang = translator.detect(text).lang
	return lang