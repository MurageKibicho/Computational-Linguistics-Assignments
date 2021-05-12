import csv
import json
import random
import numpy as np 
import random


tweetData = []


#Remove names, possible links and @'s from tweets
def CleanSingleWord(word):
	if(word[0] == "@"):
		return 0
	elif(word[:4] == 'http'):
		return 0
	elif(word == "J." or word == "j." or word == "Donald" or word == "Trump"):
		return 0
	elif(word == "Deepak" or word == "Chopra" or word == "Chrissy" or word == "Teigen"):
		return 0
	elif(word[len(word) - 1] == '.' or word[len(word) - 1] == '?' or word[len(word) - 1] == '.'):
		punc = word[len(word) - 1]
		wordWithoutPunctuation = word[:(len(word) - 1)].lower()
		return [wordWithoutPunctuation, punc]
	else:
		return word.lower() 


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

#Get bigrams from tweet data
def GenerateBigrams(tweetData):
	#Dictionary to hold bigrams
	markovDictionary = {}
	#Dictionary to store frequency counts
	wordFrequencyCounter = {}
	for line in tweetData:
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
	for line in tweetData:
		for i in range(0, len(line) - 1):
			if(line[i+1] in markovDictionary[line[i]]):
				markovDictionary[line[i]][line[i+1]] += 1
			else:
				markovDictionary[line[i]][line[i+1]] = 1

	return markovDictionary, wordFrequencyCounter

#Logic for dividing each bigram by word frequency
def FillTransitionMatrix(markovDictionary, wordFrequencyCounter):
	for firstWord in markovDictionary:
		for secondWord in markovDictionary[firstWord]:
			markovDictionary[firstWord][secondWord] /= wordFrequencyCounter[firstWord]
	return markovDictionary

#generate sentence until punctuation mark
def GenerateRandomPhrase(transitionMatrix, startWord):
	nextWord = startWord
	phrase = startWord

	while (True):
		words = []
		probabilities = []
		for word in transitionMatrix[nextWord]:
			words.append(word)
			print(transitionMatrix[nextWord][word])
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



with open("./deepakTweets.csv") as tweetFile:
	tweetReader = csv.reader(tweetFile, delimiter = ',')
	for line in tweetReader:
		if(len(line) > 0):
			if(line[0][0] != '"'):
				cleanedLine = CleanSingleLine(line) 
				tweetData.append(cleanedLine)

	markovDictionary, wordFrequencyCounter = GenerateBigrams(tweetData)
	transitionMatrix = FillTransitionMatrix(markovDictionary, wordFrequencyCounter)
	#print(transitionMatrix)
	print(GenerateRandomPhrase(transitionMatrix, "the"))


	
	#the russia-trump  collusion  

