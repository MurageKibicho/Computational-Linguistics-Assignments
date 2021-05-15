import csv
import json
import random
import numpy as np
import random
import xml.etree.ElementTree as etree
import xml.sax
import codecs
import time
import os
import pandas as pd
import bz2
import subprocess
import mwparserfromhell
import re
from timeit import default_timer as timer
import gc
import json
import pdb


def is_numeric(string):
    return bool(re.search(r'\d', string))
#def is_possessive(string):
#    return bool(re.search(r"\w+'\w+", string))
def is_empty(string):
    if string.strip() == "":
        return True
    else:
        return False

def remove_string(string):
    return is_numeric(string) or is_empty(string)


#def give_response(input):


def tokenize(data_list):
    data_tok = []
    for item in data_list:
        item = item.lower().strip().split(' ')
        temp_item = []
        for elem in item:
            if elem != "" and elem != " ":
                if elem == item[0] and elem == ",":
                    continue
                else:
                    temp_item.append(elem)
        data_tok.append(temp_item)
    return data_tok
    #data = data_tok

#data cleaning
def clean_data(item):
    item = re.sub(r'[a-z]+\*', 'AST', item)
    item = re.sub(r'[A-Z][a-z]+:', r'',item)
    item = re.sub(r'Chapter.*', '', item)
    item = re.sub(r'CHAPTER.*', '', item)
    item = re.sub(r'chapter.*', '', item)
    item = re.sub(r'\.', 'PERIOD', item)
    item = re.sub(r'\?', 'QUESTION', item)
    item = re.sub(r'\!', 'EXCLAM', item)
    item = re.sub(r'\,', ',', item)
    item = re.sub(r'(PERIOD)+', 'PERIOD', item)
    item = re.sub(r'\\\'', 'APOSTROPHE', item)
    item = re.sub(r'(\'category.*\'id.*\d.*title.*})', '', item)
    item = re.sub(r'[^\w\s]', '', item)
    item = re.sub(r'\\', '', item)
    item = re.sub(r'\n', ' ', item)
    item = re.sub(r'\t', ' ', item)
    item = re.sub(r'rnrn', ' ', item)
    item = re.sub(r'rn\srn', ' ', item)
    item = re.sub(r'\srn\s', ' ', item)
    item = re.sub(r'_', '', item)
    item = re.sub(r'(APOSTROPHE)', "'", item)
    item = re.sub(r'(PERIOD)', " . ", item)
    item = re.sub(r'(QUESTION)', " ? ", item)
    item = re.sub(r'(EXCLAM)', " ! ", item)
    item = re.sub(r'(COMMA)'," , ", item)
    item = re.sub(r'\w*AST\w*', "expletive", item)
    item = re.sub(r'\d', '', item)
    item = item.strip('body')
    item = item.strip()

    return item








#learned how to parse wikipedia data from https://towardsdatascience.com/wikipedia-data-science-working-with-the-worlds-largest-encyclopedia-c08efbac5f5c


class wiki_xml_handler(xml.sax.handler.ContentHandler):
	#use SAX parser to parse wikipedia xml data
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._pages = []
        self._articles = []
        self._article_count = 0

    def characters(self, content):
        #characters between the opening and closing tags
        if self._current_tag:
            self._buffer.append(content)

    def start_element(self, name, attrs):
		#opening tag
        if name in ('title', 'text'):
            self._current_tag = name
            self._buffer = []

    def end_element(self, name):
		#closing tag
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)

        if name == 'page':
            self._article_count += 1
            article = process_article(**self._values)
            self._articles.append(article)


def process_article(title, text, timestamp, template = 'Infobox book'):
    #using the wikipedia template, process a wikipedia article

    # Create a parsing object
    wikicode = mwparserfromhell.parse(text)

    # Search through templates for the template
    matches = wikicode.filter_templates(matches = template)

    if len(matches) >= 1:
        wikitext = wikicode.strip_code().strip()

        # Extract external links
        return (wikitext)
#Remove unwanted words from tweets
def CleanSingleLine(line):
	cleanLine = []
	if(len(line) > 0):
		if(line[0][0] != '"'):
			text = line[0].split()
			for eachWord in text:
				validWord = CleanSingleWord(eachWord)
				if(validWord != 0):
					if(isinstance(validWord ,list)):
						for eachItem in validWord:
							cleanLine.append(eachItem)
					else:
						cleanLine.append(validWord)
		return cleanLine
	else:
		return False


def find_articles(data_path, save = True):
    #combine the wiki_xml_handler class and the process_article functions
    #above to find the text for all wikipedia articles
    handler = wiki_xml_handler()

    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    start = timer()

    # Iterate through compressed file
    pdb.set_trace()
    for i, line in enumerate(subprocess.Popen(['bzcat'], stdin = open(data_path),stdout = subprocess.PIPE).stdout):

    	try:
    		parser.feed(line)
    	except StopIteration:
    		break
        # Optional limit
        #if limit is not None and len(handler.articles) >= limit:
        #    return handler._articles

    end = timer()
    articles = handler._articles
    print(f'\nFound {len(articles)} articles in {round(end - start)} seconds.')

    if save:
        #https://www.geeksforgeeks.org/writing-csv-files-in-python/
        out_file = 'articles.csv'
        start = timer()
        counter = 0
        for article in articles:
            art = str(article)
            art_list = art.split('. ')
            with open(out_file, 'w') as csvfile:
                csv_writer = csv.writer(csvfile)
                csvwriter.writerow("sentence")
                for sentence in art_list:
                    counter += 1
                    csv.writerow(sentence)
        end = timer()
        print(f'\nWrote {counter} sentences in {round(end - start)} seconds.')
    else:
        print(f'\nFound {len(articles)} articles in {round(end - start)} seconds.')
    # Memory management
    del handler
    del parser
    gc.collect()
    return None
