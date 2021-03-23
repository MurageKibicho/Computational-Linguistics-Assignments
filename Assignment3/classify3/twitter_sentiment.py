#!/usr/bin/env python3

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
import sys,os
from copy import deepcopy
from xml.etree import ElementTree

# Imports from other packages created for this homework
from classify_util import *
from twitter_util import *
from student_code import extract_features,lexicon_ratio_baseline,majority_class_baseline

#############################################################################
# Set up the options and use them to set variables appropriately
parser = get_twitter_option_parser()
(options, args) = parser.parse_args()
check_mandatory_options(parser, options, ['eval'])

eval_file = open(options.eval)

output_file = sys.stdout
if options.out != None:
    output_file = open(options.out, "w")

model_type = options.model_type
if model_type != "lex":
    check_mandatory_options(parser, options, ['train'])

verbose = options.verbose
extended_features = options.extended_features
do_subjectivity = options.twostage
smoothing_parameter = options.smoothing_value
subjectivity_threshold = options.subjectivity_threshold
polarity_threshold = options.polarity_threshold

#############################################################################
# Get training and test sets
gold_tweets = [ Tweet.fromXmlElement(x) for x in ElementTree.parse(eval_file).getroot() ]

# Create a deep copy of the gold tweets and wipe out the labels
eval_tweets = deepcopy(gold_tweets)
for tweet in eval_tweets:
    tweet.label = NO_LABEL

# Run one of the different models
if model_type == "maj":
    training_file = open(options.train)
    training_tweets = [ Tweet.fromXmlElement(x) for x in ElementTree.parse(training_file).getroot() ]
    majority_label = majority_class_baseline(training_tweets)

    for tweet in eval_tweets:
        tweet.label = majority_label

elif model_type == "lex":
    polarity_predictions = [lexicon_ratio_baseline(x) for x in eval_tweets]

    for (tweet, (label, confidence)) in zip(eval_tweets, polarity_predictions):
        tweet.label = label

else:
    training_file = open(options.train)
    training_tweets = [Tweet.fromXmlElement(x) for x in ElementTree.parse(training_file).getroot()]

    if options.auxtrain != None:
        training_tweets += [Tweet.fromXmlElement(x) for x in ElementTree.parse(options.auxtrain).getroot()]

    #############################################################################
    # Subjectivity classification (if using two phase)
    if do_subjectivity:
    
        # Create a version of the training tweets that has labels "subjective"
        # and "neutral" for doing subjectivity classification first.
        subjectivity_training_tweets = convert_posneg_to_subjective(deepcopy(training_tweets))
    
        subjectivity_training_events = \
            [extract_features(x, extended_features) + [x.label] for x in subjectivity_training_tweets]
    
        subjectivity_eval_events = \
            [extract_features(x, extended_features) + [x.label] for x in eval_tweets]
    
        subjectivity_predictions = train_and_classify(subjectivity_training_events, subjectivity_eval_events, 
                                                      model_type, smoothing_parameter, verbose)
    
        # Update the tweets with the predicted labels. Tweets that are
        # thought to be subjective are given the NO_LABEL so that they'll
        # be classified in the next phase.
        for (tweet, (label, confidence)) in zip(eval_tweets, subjectivity_predictions):
            if label == "subjective" and float(confidence) > subjectivity_threshold:
                tweet.label = NO_LABEL
            else:
                tweet.label = "neutral"

    #############################################################################
    # Polarity classification
    
    # Create a version of the training tweets for polarity
    # classification. If doing a two-stage strategy, the neutral tweets
    # are removed since neutrals were labeled in the previous stage.
    polarity_training_tweets = deepcopy(training_tweets)
    if do_subjectivity:
        polarity_training_tweets = [x for x in polarity_training_tweets if x.label != "neutral"]
    
    # Get just the unlabeled tweets for polarity classification. Note that
    # polarity_eval_tweets is a different list from eval_tweets, but that
    # the tweet object references are the same. That means that when we
    # change values to tweets in polarity_eval_tweets (like setting the
    # label to be positive or negative), we are changing the underlying
    # tweet that also lives in the eval_tweets list.
    polarity_eval_tweets = [x for x in eval_tweets if x.label == NO_LABEL ]
    
    # Create the events
    polarity_training_events = \
        [extract_features(x, extended_features) + [x.label] for x in polarity_training_tweets]
    polarity_eval_events = \
        [extract_features(x, extended_features) + [x.label] for x in polarity_eval_tweets]
    
    polarity_predictions = train_and_classify(polarity_training_events, polarity_eval_events, 
                                              model_type, smoothing_parameter, verbose)
    
    # Update the tweets with the predicted labels
    for (tweet, (label, confidence)) in zip(polarity_eval_tweets, polarity_predictions):
        if float(confidence) > polarity_threshold:
            tweet.label = label
        else:
            tweet.label = NO_LABEL

#############################################################################
# Perform evaluation

# Get the polarity results and output them.
(accuracy, label_results, correctness_vector) = scorePredictions(eval_tweets, gold_tweets)
writeResults("Polarity", accuracy, label_results, output_file)

if options.detailed_output:
    output_file.write("\n")
    
    done_right = []
    done_wrong = []
    abstentions = []
    for (correct, eval_tweet, gold_tweet) in zip(correctness_vector, eval_tweets, gold_tweets):
        if correct:
            done_right.append(gold_tweet)
        else:
            if eval_tweet.label == NO_LABEL:
                abstentions.append(gold_tweet)
            else:
                done_wrong.append((eval_tweet.label, gold_tweet))
    
    output_file.write("\n\n***************************************************\n")
    output_file.write("**          CORRECTLY LABELED TWEETS             **\n") 
    output_file.write("***************************************************\n\n")
    
    output_file.write("\n".join([t.to_string() for t in done_right]))
    
    
    output_file.write("\n\n***************************************************\n")
    output_file.write("**         INCORRECTLY LABELED TWEETS            **\n") 
    output_file.write("***************************************************\n\n")
    output_file.write("\n".join([l+" "+t.to_string() for l,t in done_wrong]))
    
    output_file.write("\n\n***************************************************\n")
    output_file.write("**                 ABSTENTIONS                   **\n") 
    output_file.write("***************************************************\n\n")
    output_file.write("\n".join([t.to_string() for t in abstentions]))

output_file.write("\n")

# Change the labels to subjective/neutral for getting subjectivity
# results. This writes over the labels in eval_tweets and gold_tweets,
# but that's okay because we're done with them now.
convert_posneg_to_subjective(eval_tweets)
convert_posneg_to_subjective(gold_tweets)
(accuracy, label_results, _) = scorePredictions(eval_tweets, gold_tweets)
writeResults("Subjectivity", accuracy, label_results, output_file)
