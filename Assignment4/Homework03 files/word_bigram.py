import re
import sys
import random
from collections import defaultdict



# defaultdict takes a lambda function as an argument and uses it to set the default value for every key
# this makes it easy to build up the dictionaries without checking for each key's existence
counts = defaultdict(lambda:0)
bicounts = defaultdict(lambda:defaultdict(lambda:0))

# this loops through all the data and stores counts
with open(sys.argv[1]) as language:
   for line in language:
       # we have to have a way to begin and end each line
       line = "# " + line.strip() + " #"
       words = re.split(r'[,.?"!\s:;]+|--', line)

       # we go through each position and keep track of word and word pair counts
       for i in range(len(words)-1):
           counts[words[i]] = counts[words[i]] + 1
           bicounts[words[i]][words[i+1]] = bicounts[words[i]][words[i+1]] + 1
        
bigram = defaultdict(lambda:{})

# this loops through all word pairs and computes relative frequency estimates
for word1 in counts:
    for word2 in bicounts[word1]:
        bigram[word1][word2] = float(bicounts[word1][word2])/float(counts[word1])
        #print("P(" + word2 + " | " + word1 + ")\tis\t" + str(bigram[word1][word2]))

# keeps generating words until # is randomly generated, then returns the whole sentence
def generate_sentence():
    sentence = "#"
    current = ''
    while current != '#':
        if current == '': current = '#'
        current = generate_next_word(current)
        sentence += " " + current
    return sentence

#given a word, randomly generates and returns the next word using the bigram model
def generate_next_word(word):
    # generate a random float between 0 and 1
    # we will use this float to probabilistically select a 'bin'
    # corresponding to a word in our bigram model
    rand = random.uniform(0,1)
    # go through each possible second word
    for following in bigram[word]:
        # subtract this word's probability from rand 
        rand -= bigram[word][following]
        # as soon as we 'cross over' zero we have found the word for that bin
        if rand < 0.0: return following
    raise ValueError("bigram[" + word + "] sums to less than 1") 


# print 20 random 'sentences' using the bigram
for i in range(20):
    print(generate_sentence())
