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
import pdb
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
	markovDictionary = {}
	#Dictionary to store frequency counts
	wordFrequencyCounter = {}
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
	markov_copy = markovDictionary.copy()
	for firstWord in markovDictionary:
		for secondWord in markovDictionary[firstWord]:
			prob = np.true_divide(markovDictionary[firstWord][secondWord],wordFrequencyCounter[firstWord])
		#lambda smoothing
		if prob > lam_bound:
			prob = prob - lam
		elif prob < lam_bound:
			prob = prob + lam
		markovDictionary[firstWord][secondWord] = prob
		transitionMatrix = markovDictionary
		markovDictionary = markov_copy
	return transitionMatrix


def UpdateTransitionMatrix(transitionMatrix, markovDictionary, wordFrequencyCounter, topic_dict, topic_freqcounts):
	lam, lam_bound = .00005, .0001

	for firstWord in topic_dict:
		for secondWord in topic_dict[firstWord]:
			topic_prob = np.true_divide(topic_dict[firstWord][secondWord],topic_freqcounts[firstWord])
			if topic_prob > lam_bound:
				topic_prob = topic_prob - lam
			elif topic_prob < lam_bound:
				topic_prob = topic_prob + lam

			if firstWord in transitionMatrix.keys():
				if secondWord in transitionMatrix[firstWord].keys():
					combined_bigram_count = topic_dict[firstWord][secondWord] + markovDictionary[firstWord][secondWord]
					combined_word_count = topic_freqcounts[firstWord] + wordFrequencyCounter[firstWord]
					topic_dict[firstWord][secondWord]= np.true_divide(combined_bigram_count, combined_word_count)

				else:
					topic_dict[firstWord][secondWord] = topic_prob
			else:
				topic_dict[firstWord][secondWord] = topic_prob

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
			probabilities.append(transitionMatrix[nextWord][word])

		#If current word does not have a bigram, break
		if not probabilities:
			break
		nextWord = np.random.choice(words, 1, probabilities)[0]
		phrase += " " + nextWord + " "
		if(nextWord == '!' or nextWord == '.' or nextWord == '?' or nextWord == ' ! ' or nextWord == ' . ' or nextWord == ' ? '):
			break
	return phrase

def get_topic_data(txt):
	data_list = []
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
				item = re.sub(r'\\', '', item)
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
	return data_list

def get_likelihood(sentence, probability_matrix):
	if type(sentence) == list:
		phrase_temp = sentence
	else:
		phrase_temp = sentence.split(" ")
	phrase_list = []
	for word in phrase_temp:
		if word != "" and word != " ":
			phrase_list.append(word)
	bis = []
	for i in range(len(phrase_list)):
		if i+1 < len(phrase_list):
			bi = (phrase_list[i], phrase_list[i+1])
			bis.append(bi)
	temp_probs = []
	for item in bis:
		first_word = item[0]
		second_word = item[1]
		prob = topic_matrix[first_word][second_word]
		log_prob = np.log(prob)
		temp_probs.append(log_prob)
	likelihood = np.exp(np.sum(temp_probs))

	return likelihood

#def update_transition_matrix(transitionMatrix, )
start = timer()
print("generating language model...")

markovDictionary, wordFrequencyCounter = GenerateBigrams(brown.sents())
transitionMatrix = FillTransitionMatrix(markovDictionary, wordFrequencyCounter)

end = timer()
print(len(brown.sents()),"sentences parsed in",(end-start),"seconds")

categories = ['jokes', 'sci_fi', 'regency_england','finance', 'medicine']


print("What flavor of 'bullshit' would you like today? \n Your options are:")
print("")
for category in categories:
	print("\t category name:",category)
print("you can quit at any time by entering 'quit'")
print("call by entering the category name: ")
txt = input("> ")
while not txt == "quit":
	#get topic data and tokenize it so that data_tok is a list of lists,
	#with sublists all of form ['word', 'word', 'word'], each sublist comprising a sentence
	data_list = get_topic_data(txt)
	data_tok = tokenize(data_list)

	#calculate bigram counts and probabilities for topic data
	topic_dict, topic_freqcounts = GenerateBigrams(data_tok)
	topic_matrix = UpdateTransitionMatrix(transitionMatrix, markovDictionary, wordFrequencyCounter, topic_dict, topic_freqcounts)

	#select a start word
	total_count = 0
	for item in topic_freqcounts.keys():
		total_count += topic_freqcounts[item]
	topic_probs = []
	words_list = []
	for item in topic_freqcounts.keys():
		temp_prob = np.divide(topic_freqcounts[item], total_count)
		topic_probs.append(temp_prob)
		words_list.append(item)
	start_value = np.random.choice(words_list, 1, p=topic_probs)
	start_value = str(start_value[0])

	#generate bullshit
	generated_phrase = GenerateRandomPhrase(topic_matrix, start_value)

	#calculate likelihood of generating bullshit sentence, a random sentence from the text,
	#and the mean likelihood of generating each sentence in the text
	gen_likelihood = get_likelihood(generated_phrase, topic_matrix)
	rand_ind = np.random.choice(len(data_tok))
	comp_likelihood = get_likelihood(data_tok[rand_ind], topic_matrix)

	likelihoods = []
	for sentence in data_tok:
		val = get_likelihood(sentence, topic_matrix)
		likelihoods.append(val)
	mean_likelihood = np.mean(likelihoods)

	#print results
	print("your bullshit, freshly served: \n \t", generated_phrase)
	print("the likelihood of generating this sentence: \n \t", gen_likelihood)
	print("the likelihood of generating a randomly selected sentence actually present in the text: \n \t", comp_likelihood)
	print("the mean likelihood of generating the sentences in the text: \n \t", mean_likelihood)

	#allow user to continue as many times as they want
	txt = input("> ")


print("Thank you for your time. \n Enjoy the perpetual struggle to make meaning in a huge and chaotic world!\n")



