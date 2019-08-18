import wikipedia
from googlesearch import search
from duckduckpy import query
import re
from readability import Document
import requests
import json
from App_files.nlp_helpers import summerize_content
def search_duckduckgo(search_word):
	response = query(search_word, container="dict")['abstract']
	return response

def get_wiki_page(search_word):
	top_result = wikipedia.page(search_word)
	print(top_result.url)
	return top_result.url

def get_google_results(search_word):
	results = []
	# removing youtube urls
	for result in search(search_word, stop=5):
		print("google search result", result)
		if not re.match(r"https://www.youtube", result):
			results.append(result)
	return results

def get_main_text(url):
    response = requests.get(url)
    doc = Document(response.text)
    text = doc.summary()
    re_form = r'(?<=<p>)(.*?)(?=</p>)'
    re_text = " ".join(re.findall(re_form, text))
    print(re_text)
    return re_text

def get_wiki_info(query):
    wiki_page = get_wiki_page(query)
    main_text = get_main_text(wiki_page)
    info = json.loads(summerize_content(main_text))['summary']
    return info 

def get_google_info(query):
    # moving wiki links ahead
    results = get_google_results(query)
    for result in results:
        if (re.search('wikipedia', result)):
            results.insert(0, results.pop(results.index(result)))

    for result in results:
        main_text = get_main_text(result)
        info = json.loads(summerize_content(main_text, 3))['summary']
        if (len(info) != 0):
            break
    return info
