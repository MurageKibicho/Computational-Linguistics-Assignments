from __future__ import division

#############################################################################
# Copyright 2011 Jason Baldridge
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

# Imports from Python standard libraries
import re,math
from operator import itemgetter

# Imports from external packages included in the same directory
from porter_stemmer import PorterStemmer
import twokenize
import emoticons

# Imports from other packages created for this homework
from classify_util import makefeat,window

#############################################################################
# Code to set up some resources for your features

# Create the stemmer for later use.
stemmer = PorterStemmer()

# Read in the stop words
stop_words = set([x.strip() for x in open("data/resources/stopwords.english", encoding="ISO-8859-1").readlines()])

# Obtain the words from Opinion Lexicon
neg_words =  set([x.strip() for x in open("data/resources/negative-words.txt", encoding="ISO-8859-1").readlines() if not(x.startswith(";"))])
neg_words.remove("")

pos_words =  set([x.strip() for x in open("data/resources/positive-words.txt", encoding="ISO-8859-1").readlines() if not(x.startswith(";"))])
pos_words.remove("")


#############################################################################
# Add your regular expressions here.


#############################################################################
# General features (for both subjectivity and polarity)
def extract_features (tweet, extended_features):
	features = []
	lctokens=[]
	stems=[]
	# FIXME: Change to use tokenization from twokenize.
	tokens = twokenize.tokenize(tweet.content)
	for i in tokens:
		lctokens.append(i.lower())
	
	for i in lctokens:
		stems.append(stemmer.stem_token(i))
	

	# Add unigram features. 
	for i in stems:
	 	if(i in stop_words):
	 		stems.remove(i)

	# FIXME: consider using lower case version and/or stems
	features.extend([makefeat("word",tok) for tok in stems])

	# The same thing, using a for-loop (boooring!)
	#for tok in tokens:
	#    features.append(makefeat("word",tok))
	
	nouns = []
	if extended_features:
		for i in tokens:
			if(i[0].isupper()):
				nouns.append(i)

		# FIXME: Add bigram features (suggestion: use the window function in classify_utils.py)
	

		# FIXME: Add other features -- be creative!

	return features


#############################################################################
# Predict sentiment based on ratio of positive and negative terms in a tweet
def majority_class_baseline (tweetset):
	positiveLabel = 0
	negativeLabel = 0
	neutralLabel = 0
	
	for tweet in tweetset:
		if tweet.label == "positive":
			positiveLabel += 1
		elif tweet.label == "negative":
			negativeLabel += 1
		elif tweet.label == "neutral":
			neutralLabel += 1


	if (positiveLabel >= negativeLabel) and (positiveLabel >= neutralLabel):
		majority_class_label = "positive"
	elif (negativeLabel >= positiveLabel) and (negativeLabel >= neutralLabel):
		majority_class_label = "negative"
	elif (neutralLabel >= positiveLabel) and (neutralLabel >= negativeLabel):
		majority_class_label = "neutral"
	
	
	return majority_class_label


#############################################################################
# Predict sentiment based on ratio of positive and negative terms in a tweet
def lexicon_ratio_baseline (tweet):
	num_positive = 0
	num_negative = 0

	# FIXME: Change to use tokenization from twokenize

	tokens = twokenize.tokenize(tweet.content)
	# FIXME: Count the number of positive and negative words in the tweet
	
	for i in tokens:
		if i in neg_words:
			num_negative+=1
		elif i in pos_words:
			num_positive+=1
	


	#########################################################################
	# Don't change anything below this comment
	#########################################################################

	# Let neutral be prefered if nothing is found.
	num_neutral = .2

	# Go with neutral if pos and neg are the same
	if num_positive == num_negative:
		num_neutral += len(tokens)

	# Add a small count to each so we don't get divide-by-zero error
	num_positive += .1
	num_negative += .1

	denominator = num_positive + num_negative + num_neutral

	# Create pseudo-probabilities based on the counts
	predictions = [("positive", num_positive/denominator), 
				   ("negative", num_negative/denominator),
				   ("neutral", num_neutral/denominator)]

	# Sort
	predictions.sort(key=itemgetter(1),reverse=True)

	# Return the top label and its confidence
	return predictions[0]
	
