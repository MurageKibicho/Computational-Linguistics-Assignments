import csv
import json
import random
import numpy as np
import os
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import re
from nltk.corpus import brown
from markov_utils import remove_string
from markov_utils import is_numeric
from markov_utils import is_empty
from markov_utils import clean_data
from markov_utils import tokenize
from timeit import default_timer as timer
from collections import defaultdict
import itertools as it

def GenerateBigrams(data):
	#Dictionary to hold bigrams
	markovDictionary = defaultdict(lambda: 1)
	#Dictionary to store frequency counts
	wordFrequencyCounter = defaultdict(lambda: 1)
	for line in data:
		#Count word frequencies
		for eachWord in line:
			if eachWord in wordFrequencyCounter:
				wordFrequencyCounter[eachWord] += 1
			else:
				wordFrequencyCounter[eachWord] = 1
		#Initialize bigram dictionary
		for i in range(0, len(line)):
			markovDictionary[line[i]] = {}
	#Logic for creating bigrams
	for line in data:
		for i in range(0, len(line) - 1):
			if(line[i+1] in markovDictionary[line[i]]):
				markovDictionary[line[i]][line[i+1]] += 1
			else:
				markovDictionary[line[i]][line[i+1]] = 1

	return markovDictionary, wordFrequencyCounter

def FillTransitionMatrix(markovDictionary, wordFrequencyCounter):
	lam, lam_bound = .00005, .0001
	for firstWord in markovDictionary:
		for secondWord in markovDictionary[firstWord]:
			prob = markovDictionary[firstWord][secondWord] // wordFrequencyCounter[firstWord]
		#lambda smoothing
		if prob > lam_bound:
			prob = prob - lam
		elif prob < lam_bound:
			prob = prob + lam
		markovDictionary[firstWord][secondWord] = np.log(prob)
	return markovDictionary


	return markovDictionary
def UpdateTransitionMatrix(markovDictionary, wordFrequencyCounter, topic_dict, topic_freqcounts):
	lam, lam_bound = .00005, .0001
	for firstWord in topic_dict:
		for secondWord in topic_dict[firstWord]:
			topic_prob = topic_dict[firstWord][secondWord] // topic_freqcounts[firstWord]
			if topic_prob > lam_bound:
				topic_prob = topic_prob - lam
			elif topic_prob < lam_bound:
				topic_prob = topic_prob + lam

			if firstWord in markovDictionary.keys():
				if secondWord in markovDictionary[firstWord].keys():
					topic_dict[firstWord][secondWord] = np.log(topic_prob) + markovDictionary[firstWord][secondWord]
				else:
					topic_dict[firstWord][secondWord] = np.log(topic_prob)
			else:
				topic_dict[firstWord][secondWord] = np.log(topic_prob)
	return topic_dict


#generate sentence until punctuation mark
def GenerateRandomPhrase(transitionMatrix, startWord):
	nextWord = startWord
	phrase = startWord

	while (True):
		words = []
		probabilities = []
		for word in transitionMatrix[nextWord]:
			words.append(word)
			#print(transitionMatrix[nextWord][word])
			probabilities.append(transitionMatrix[nextWord][word])

		#If current word does not have a bigram, break
		if not probabilities:
			print("Empty")
			break
		nextWord = np.random.choice(words, 1, probabilities)[0]
		phrase += " " + nextWord + " "
		if(nextWord == '!' or nextWord == '.' or nextWord == '?' or nextWord == ' ! ' or nextWord == ' . ' or nextWord == ' ? '):
			break
	return phrase

#def update_transition_matrix(transitionMatrix, )
start = timer()
print("generating language model...")

markovDictionary, wordFrequencyCounter = GenerateBigrams(brown.sents())
transitionMatrix = FillTransitionMatrix(markovDictionary, wordFrequencyCounter)

end = timer()
print(len(brown.sents()),"sentences parsed in",(end-start),"seconds")

categories = ['jokes', 'sci_fi', 'regency_england','finance', 'medicine']

#if __name__ == "__main__":
print("What flavor of bullshit would you like today? \n Your options are:")
print("")
for category in categories:
    print("\t category name:",category)
print("you can quit at any time by entering 'quit'")
print("call by entering the category name: ")
txt = input("> ")
print("category selected:",txt)
#while not txt == "quit":
if txt == 'jokes':
    with open('wocka.json') as f:

        data = json.load(f)
        data_list = []
        for item in data:
            item = str(item)
            item = clean_data(item)

            if item != "":
                sentences = re.split(r'(\.|\!|\?)',item)
                for i, sentence in enumerate(sentences):
                    if sentence.split(" ")[0] == ',':
                        sentence = sentence[1:]
                    if len(sentence) > 1:
                        if i+1 < len(sentences):
                            sentence = sentences[i] + sentences[i+1]
                        data_list.append(sentence)

elif txt == "sci_fi":
    with open('all_series_lines.json') as f:
        data = json.load(f)
        data_list = []
        for key in data.keys():
            series = data[key]
            for nest_key in series.keys():
                episode = series[nest_key]
                for speaker in episode.keys():
                    item = episode[speaker]
                    #print(item)
                    item = str(item)
                    item = clean_data(item)
                    if item != "":
                        sentences = re.split(r'(\.|\!|\?)',item)
                        for i, sentence in enumerate(sentences):
                            if sentence.split(" ")[0] == ',':
                                sentence = sentence[1:]
                            if len(sentence) > 1:
                                if i+1 < len(sentences):
                                    sentence = sentences[i] + sentences[i+1]
                                data_list.append(sentence)

elif txt == "regency_england":
    data_list = []
    for filename in os.listdir('austen'):
        if filename.endswith(".txt"):
            path = "austen/"+str(filename)
            with open(path) as f:
                item = f.read()
                item = clean_data(item)
                if item != "":
                    sentences = re.split(r'(\.|\!|\?)',item)
                    for i, sentence in enumerate(sentences):
                        if sentence.split(" ")[0] == ',':
                            sentence = sentence[1:]
                        if len(sentence) > 1:
                            if i+1 < len(sentences):
                                sentence = sentences[i] + sentences[i+1]
                            data_list.append(sentence)

elif txt == "finance":
    data_list = []
    with open("analyst_ratings_processed.csv") as f:
        reader = csv.reader(f)
        for item in reader:
            #print(item)
            item = str(item[1])
            item = re.sub(r'\d', '', item)
            item = re.sub(r'\$', '', item)
            item = re.sub(r'\#', '', item)
            item = re.sub(r'\%', '', item)
            item = re.sub(r'\d', '', item)
            item = re.sub(r'-', '', item)
            item = re.sub(r'[^\w\s]', '', item)
            item = re.sub(r'title', '', item)
            data_list.append(item)

elif txt == "medicine":
    data_list = []
    with open("mtsamples.csv") as f:
        reader = csv.reader(f)
        for item in reader:
            item = item[4]
            item = clean_data(item)
            if item != "":
                sentences = re.split(r'(\.|\!|\?)',item)
                for i, sentence in enumerate(sentences):
                    if sentence.split(" ")[0] == ',':
                        sentence = sentence[1:]
                    if len(sentence) > 1:
                        if i+1 < len(sentences):
                            sentence = sentences[i] + sentences[i+1]
                        data_list.append(sentence)
elif txt == "quit":
	print("Thank you for your time. \n Enjoy the perpetual struggle to make meaning in a huge and chaotic world!\n")



data_tok = tokenize(data_list)





topic_dict, topic_freqcounts = GenerateBigrams(data_tok)
topic_matrix = UpdateTransitionMatrix(markovDictionary, wordFrequencyCounter, topic_dict, topic_freqcounts)
print(GenerateRandomPhrase(topic_matrix, "the"))
#topic_probs

#markovDictionary, wordFrequencyCounter = GenerateBigrams(brown.sents())
#transitionMatrix = FillTransitionMatrix(markovDictionary, wordFrequencyCounter)



print("Thank you for your time. \n Enjoy the perpetual struggle to make meaning in a huge and chaotic world!\n")




#topic_dict, topic_freqcounts = GenerateBigrams(data)

#print(transitionMatrix)
#print(GenerateRandomPhrase(transitionMatrix, "the"))
