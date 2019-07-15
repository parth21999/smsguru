from googletrans import Translator
from rake_nltk import Rake
import re 
'''
def get_keywords(text):
	r = Rake()
	r.extract_keywords_from_text(text)
	return " ".join(r.get_ranked_phrases())

rake = Rake()
translator = Translator()
text = 'quadratic equation solve kaise karte hain'
keywords = get_keywords(text)
translation = translator.translate(text)
print(keywords)
print(translation)
'''

def remove_youtube_results(results):
    final_results = []
    for result in results: 
        if not re.match(r"https://www.youtube.com", result):
            final_results.append(result)
    return final_results

results = ['a', 'b', 'c', 'https://www.youtube.com/watch v=Y8Aliq-ZbZk']
print(remove_youtube_results(results))

