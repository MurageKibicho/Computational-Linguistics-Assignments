import re
import sys
import random
from collections import defaultdict
import numpy as np
import math



if (sys.argv[2] == '2'):
	counts = defaultdict(lambda:0)
	bigramCounts = defaultdict(lambda:defaultdict(lambda:0))
	bigram = defaultdict(lambda:{})
	runningProbability = 0
	qCounter = 0

	with open(sys.argv[1]) as language:
		for line in language:
			line = line.strip()
			words = re.split(r'[,.?"!\s:;]+|--', line)

			for i in range(len(words) - 1):
				counts[words[i]]+= 1
				bigramCounts[words[i]][words[i+1]] += 1
	for word1 in counts:
		for word2 in bigramCounts[word1]:
			bigram[word1][word2] = float(bigramCounts[word1][word2])/float(counts[word1])
		#print("P(" + word2 + " | " + word1 + ")\tis\t" + str(bigram[word1][word2]))
	if (len(sys.argv) == 4):
		bigramList = []
		with open(sys.argv[3]) as testFile:
			for eachLine in testFile:
				eachLine = eachLine.strip()
				lineWords = re.split(r'[,.?"!\s:;]+|--', eachLine)

				for i in range(len(lineWords) - 1):
					if i < (len(lineWords) - 1):
						bigramList.append((lineWords[i], lineWords[i+1]))
			#print(bigramList)

				print(lineWords, end=' ')
				for i in range(len(bigramList)):
					temporaryProbability = 0
					if bigramList[i][0] in bigram:
						if bigramList[i][1] in bigram[bigramList[i][0]]:
							temporaryProbability+= np.log2((bigram[bigramList[i][0]][bigramList[i][1]]))
							#print("(" + bigramList[i][0] + "|" + bigramList[i][1] + ")" + str(bigram[bigramList[i][0]][bigramList[i][1]]))
							runningProbability += temporaryProbability
							qCounter +=1
							#print(np.log2((bigram[bigramList[i][0]][bigramList[i][1]])))
						else:
							#print("(" + bigramList[i][0] + "|" + bigramList[i][1] + ")" + '0')
							temporaryProbability+= -math.inf
							runningProbability += temporaryProbability
							qCounter +=1
				print(np.exp2(temporaryProbability))
			print("Perplexity:" +str(np.exp2(runningProbability/qCounter)))                          

	def generate_sentence():
		sentence = "# #"
		current = ''
		while current != '#':
			if current == '': 
				current = '#'
			current = generate_next_word(current)
			sentence += " " + current
		return sentence

	#given a word, randomly generates and returns the next word using the bigram model
	def generate_next_word(word):
		rand = random.uniform(0,1)
		for following in bigram[word]:
			rand -= bigram[word][following]
			if rand < 0.0:
				return following
		raise ValueError("bigram[" + word + "] sums to less than 1") 

	if(len(sys.argv) == 3):
		for i in range(25):
			print(generate_sentence())

elif (sys.argv[1] == '-add1' and sys.argv[3] == '2'):
	counts = defaultdict(lambda:0)
	bigramCounts = defaultdict(lambda:defaultdict(lambda:0))
	bigram = defaultdict(lambda:{})
	runningProbability = 0
	qCounter = 0

	with open(sys.argv[2]) as language:
		for line in language:
			line = line.strip()
			words = re.split(r'[,.?"!\s:;]+|--', line)

			for i in range(len(words) - 1):
				counts[words[i]]+= 1
				bigramCounts[words[i]][words[i+1]] += 1
	for word1 in counts:
		for word2 in bigramCounts[word1]:
			bigram[word1][word2] = float(bigramCounts[word1][word2] + 1)/float(counts[word1])
		#print("P(" + word2 + " | " + word1 + ")\tis\t" + str(bigram[word1][word2]))
	if (len(sys.argv) == 5):
		bigramList = []
		with open(sys.argv[4]) as testFile:
			for eachLine in testFile:
				eachLine = eachLine.strip()
				lineWords = re.split(r'[,.?"!\s:;]+|--', eachLine)

				for i in range(len(lineWords) - 1):
					if i < (len(lineWords) - 1):
						bigramList.append((lineWords[i], lineWords[i+1]))
			#print(bigramList)

				print(lineWords, end=' ')
				for i in range(len(bigramList)):
					temporaryProbability = 0
					if bigramList[i][0] in bigram:
						if bigramList[i][1] in bigram[bigramList[i][0]]:
							temporaryProbability+= np.log2((bigram[bigramList[i][0]][bigramList[i][1]]))
							#print("(" + bigramList[i][0] + "|" + bigramList[i][1] + ")" + str(bigram[bigramList[i][0]][bigramList[i][1]]))
							runningProbability += temporaryProbability
							qCounter +=1
							#print(np.log2((bigram[bigramList[i][0]][bigramList[i][1]])))
						else:
							#print("(" + bigramList[i][0] + "|" + bigramList[i][1] + ")" + '0')
							temporaryProbability+= -math.inf
							runningProbability += temporaryProbability
							qCounter +=1
				print(np.exp2(temporaryProbability))
			print("Perplexity:" +str(np.exp2(runningProbability/qCounter)))                          

	def generate_sentence():
		sentence = "# #"
		current = ''
		while current != '#':
			if current == '': 
				current = '#'
			current = generate_next_word(current)
			sentence += " " + current
		return sentence

	#given a word, randomly generates and returns the next word using the bigram model
	def generate_next_word(word):
		rand = random.uniform(0,1)
		for following in bigram[word]:
			rand -= bigram[word][following]
			if rand < 0.0:
				return following
		raise ValueError("bigram[" + word + "] sums to less than 1") 

	if(len(sys.argv) == 4):
		for i in range(25):
			print(generate_sentence())


elif(sys.argv[2] == '3'):
	trigram = defaultdict(lambda:defaultdict(lambda:{}))
	bigramCounts = defaultdict(lambda:defaultdict(lambda:0))
	trigramCounts = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))
	runningProbability = 0
	qCounter = 0

	with open(sys.argv[1]) as language:
		for line in language:
			line = '# ' + line.strip()
			words = re.split(r'[,.?"!\s:;]+|--', line)

			for i in range(len(words)-2):
				bigramCounts[words[i]][words[i+1]] += 1
				trigramCounts[words[i]][words[i+1]][words[i+2]] += 1

	for word1 in bigramCounts:
		for word2 in bigramCounts[word1]:	
			for word3 in trigramCounts[word1][word2]:
				trigram[word1][word2][word3] = float(trigramCounts[word1][word2][word3])/float(bigramCounts[word1][word2])

	if (len(sys.argv) == 4):
		trigramList = []
		with open(sys.argv[3]) as testFile:
			for eachLine in testFile:
				eachLine = eachLine.strip()
				lineWords = re.split(r'[,.?"!\s:;]+|--', eachLine)

				for i in range(len(lineWords) - 2):
					if i < (len(lineWords) - 2):
						trigramList.append((lineWords[i], lineWords[i+1], lineWords[i+2]))
			#print(trigramList)

				print(lineWords, end=' ')
				for i in range(len(trigramList)):
					temporaryProbability = 0
					if trigramList[i][0] in trigram:
						if trigramList[i][1] in trigram[trigramList[i][0]]:
							if trigramList[i][2] in trigram[trigramList[i][0]][trigramList[i][1]]:
								temporaryProbability+= np.log2((trigram[trigramList[i][0]][trigramList[i][1]][trigramList[i][2]]))
								qCounter +=1
								runningProbability += temporaryProbability
						#print(np.log2((bigram[bigramList[i][0]][bigramList[i][1]])))
						else:
							temporaryProbability+= -math.inf
							runningProbability += temporaryProbability
							qCounter +=1
				print(np.exp2(temporaryProbability))
			print("Perplexity:" +str(np.exp2(runningProbability/qCounter)))                               
	def generate_sentence():
		sentence = "# #"
		current = ''
		while current != '#':
			if current == '': 
				current = '#'				
			senList  = sentence.split()
			previousCurrent = senList[-2]
			current = generate_next_word(previousCurrent, current)
			sentence += " " + current
		return sentence

	#given a word, randomly generates and returns the next word using the bigram model
	def generate_next_word(word1, word2):
		rand = random.uniform(0,1)
		for following in trigram[word1][word2]:
			rand -= trigram[word1][word2][following]
			if rand < 0.0:
				return following
		raise ValueError("bigram[" + word + "] sums to less than 1") 

	if (len(sys.argv) == 3):
		for i in range(25):
			print(generate_sentence())

elif (sys.argv[1] == '-add1' and sys.argv[3] == '3'):
	trigram = defaultdict(lambda:defaultdict(lambda:{}))
	bigramCounts = defaultdict(lambda:defaultdict(lambda:0))
	trigramCounts = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))
	runningProbability = 0
	qCounter = 0

	with open(sys.argv[2]) as language:
		for line in language:
			line = '# ' + line.strip()
			words = re.split(r'[,.?"!\s:;]+|--', line)

			for i in range(len(words)-2):
				bigramCounts[words[i]][words[i+1]] += 1
				trigramCounts[words[i]][words[i+1]][words[i+2]] += 1

	for word1 in bigramCounts:
		for word2 in bigramCounts[word1]:	
			for word3 in trigramCounts[word1][word2]:
				trigram[word1][word2][word3] = float(trigramCounts[word1][word2][word3] + 1)/float(bigramCounts[word1][word2])

	if (len(sys.argv) == 5):
		trigramList = []
		with open(sys.argv[4]) as testFile:
			for eachLine in testFile:
				eachLine = eachLine.strip()
				lineWords = re.split(r'[,.?"!\s:;]+|--', eachLine)

				for i in range(len(lineWords) - 2):
					if i < (len(lineWords) - 2):
						trigramList.append((lineWords[i], lineWords[i+1], lineWords[i+2]))
			#print(trigramList)

				print(lineWords, end=' ')
				for i in range(len(trigramList)):
					temporaryProbability = 0
					if trigramList[i][0] in trigram:
						if trigramList[i][1] in trigram[trigramList[i][0]]:
							if trigramList[i][2] in trigram[trigramList[i][0]][trigramList[i][1]]:
								temporaryProbability+= np.log2((trigram[trigramList[i][0]][trigramList[i][1]][trigramList[i][2]]))
								qCounter +=1
								runningProbability += temporaryProbability
						#print(np.log2((bigram[bigramList[i][0]][bigramList[i][1]])))
						else:
							temporaryProbability+= -math.inf
							runningProbability += temporaryProbability
							qCounter +=1
				print(np.exp2(temporaryProbability))
			print("Perplexity:" +str(np.exp2(runningProbability/qCounter)))                               
	def generate_sentence():
		sentence = "# #"
		current = ''
		while current != '#':
			if current == '': 
				current = '#'				
			senList  = sentence.split()
			previousCurrent = senList[-2]
			current = generate_next_word(previousCurrent, current)
			sentence += " " + current
		return sentence

	#given a word, randomly generates and returns the next word using the bigram model
	def generate_next_word(word1, word2):
		rand = random.uniform(0,1)
		for following in trigram[word1][word2]:
			rand -= trigram[word1][word2][following]
			if rand < 0.0:
				return following
		raise ValueError("bigram[" + word + "] sums to less than 1") 

	if (len(sys.argv) == 4):
		for i in range(25):
			print(generate_sentence())

			

