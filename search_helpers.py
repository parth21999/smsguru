import wikipedia
from googlesearch import search
from duckduckpy import query
import re
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