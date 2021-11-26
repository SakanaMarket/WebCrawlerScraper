import os
import re
import nltk
import json
import _pickle
import sys
import unicodedata
import copy
from datetime import datetime
from lxml import html
from lxml.html.clean import Cleaner
from urllib.parse import urlparse
from collections import defaultdict

leon_dict = defaultdict(list)
doc_id = 0

class Posting:
	def __init__(self, doc_id, tfidf, op):
		self.doc_id = doc_id
		self.tfidf = tfidf
		self.important = op
	def __repr__(self):
		return "({}, {}, {})".format(self.doc_id, self.tfidf, self.important)
	

def tokenize(j_file):
	a_flag = True
	u_flag = True
	global leon_dict, doc_id
	with open(j_file) as j:
		data = json.load(j)
		url = data["url"]
		
		if data["encoding"].lower() != "utf-8" and data["encoding"].lower() != "ascii":
			return False

		saved = data["content"] ##.replace("[\'\"](\\u(\w*)*)+[\'\"]", "")

		saved = re.sub(r"([\w]*[^\x00-\x7F]+[\w]*)", "", saved)
		saved = "".join(ch for ch in saved if unicodedata.category(ch)[0]!="C")
##		saved = re.sub(r"\t|\n|\r|\.|\{|\}", " ", saved)

##		saved2 = copy.deepcopy(saved)

		if data["encoding"].lower() == "ascii":
			saved = saved.encode("ascii")
		elif data["encoding"].lower() == "utf-8":
			saved = saved.encode("utf-8", "ignore")

		doc = html.fromstring(saved)

		body = Cleaner( style=True, links=True, scripts=True, javascript=True, remove_unknown_tags=True)
		body.kill_tags = ["h1", "h2", "h3", "h4", "h5", "h6", "strong", "em", "title", "A"]
			
		important = Cleaner( style=True, links=True, scripts=True, javascript=True, remove_unknown_tags=False )
		important.allow_tags = ["h1", "h2", "h3", "h4", "h5", "h6", "strong", "em", "title", "body"]
		important.kill_tags = ["canvas", "A"]

		sno = nltk.stem.SnowballStemmer('english')

		bod = [ re.sub(r"\t|\n|\.", " ", x.text).strip() for x in body.clean_html( doc ).xpath("//body//*") if x.text ]
		imp = [ re.sub(r"\t|\n|\.", " ", x.text).strip() for x in important.clean_html( doc ).xpath("//body//*") if x.text ]

		s1 = [ sno.stem(word.lower()) for line in imp for word in re.findall("[a-zA-Z\d\.]{3,}", line) if line ]
		s2 = [ sno.stem(word.lower()) for line in bod for word in re.findall("[a-zA-Z\d\.]{3,}", line) if line ]

		word_dict = defaultdict(int)

		for x in s1:
#			print(x)
			word_dict[x]+=1
		for y in s2:
#			print(y)
			word_dict[y]+=1
		
		s2 = set(s2)-set(s1)
		s1 = set(s1)

		for word in s2:
#			print(word)
			leon_dict[word].append(Posting(doc_id, word_dict[word], 0))
		for word in s1:
#			print(word)
			leon_dict[word].append(Posting(doc_id, word_dict[word], 1))
		return True
		
		
# 8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json

if __name__ == '__main__':
	count = 0
	for subdir, dirs, files in os.walk("/home/lopes/Datasets/IR/DEV"):
##		if count >= 10: break
		for file in files:
##			if count >= 10: break
			print(datetime.now(), os.path.join(subdir, file))
#                       s = os.path.getsize(os.path.join(subdir, file))
			if tokenize(os.path.join(subdir, file)):
				count+=1
#			else:
#                               with open("large.txt", "a") as l:
#                                       l.write(os.path.join(subdir, file))

	with open("dump.pickle", "wb") as d:
		_pickle.dump(leon_dict, d)
	with open("out.txt", "w") as o:
		o.write("Length of Dict: {}\nTotal Files counted: {}\n".format(len(leon_dict), count))
