#!/usr/bin/env python3

#############################################################################
# Copyright 2011 Jason Baldridge
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#############################################################################

from __future__ import division
import sys
from operator import itemgetter
from classify_util import *

#############################################################################
# Get the options

parser = get_categorizer_option_parser()
(options, args) = parser.parse_args()
check_mandatory_options(parser, options, ['train', 'predict'])

#############################################################################
# Use the options to set the input and output files appropriately

training_file = open(options.train)
prediction_file = open(options.predict)
output_file = sys.stdout
if options.out != None:
    output_file = open(options.out, "w")

verbose = options.verbose
errmsg("Showing verbose output.", verbose)
# NOTE: to create debugging output, use errmsg() at the appropriate
# places in the code and use the -v (--verbose) option when you call
# the program.

lambda_value = 0.0
if options.lambda_value != None:
    lambda_value = options.lambda_value

################################################################################
# Use the frequencies to determine the parameters of the model

training_data = read_data(training_file)

l_freq = {}     # label frequencies
al_freq = {}    # attribute-label frequencies
avl_freq = {}   # attribute-value-label frequencies

av_sets = {}    # attribute-value sets

all_labels = set([])
all_attributes = set([])

for avs,label in training_data:

    all_labels.add(label)
    
    l_freq[label] = l_freq.get(label,0) + 1
    for av in avs:
        attr,val = av.split('=')
        all_attributes.add(attr)
        al_freq[(attr,label)] = al_freq.get((attr,label),0) + 1
        avl_freq[(attr,val,label)] = avl_freq.get((attr,val,label),0) + 1

        if attr in av_sets:
            av_sets[attr].add(val)
        else:
            av_sets[attr] = set([val])

av_sizes = {}
for attr in av_sets.keys():
    av_sizes[attr] = len(av_sets[attr]) + 1   # +1 to account for the unknown value
        
num_instances = len(training_data)
labels = l_freq.keys()

################################################################################
# Use the frequencies to determine the parameters of the model

parameters = {}
for label in l_freq.keys():
    parameters[label] = math.log((l_freq[label] + lambda_value) /
                                 (num_instances + lambda_value * len(labels)))

for attr,val,label in avl_freq.keys():
    parameters[(attr,val,label)] = \
          math.log((avl_freq[(attr,val,label)] + lambda_value )
                   / (al_freq[(attr,label)] + lambda_value * av_sizes[attr]))

unknown_parameters = {}
if lambda_value == 0:
    for attr,label in al_freq.keys():
        unknown_parameters[(attr,label)] = -50
else:
    for attr,label in [(attr,label) for attr in all_attributes for label in all_labels]:
        unknown_parameters[(attr,label)] = \
              math.log(lambda_value / (al_freq.get((attr,label),0.0) + lambda_value * av_sizes[attr]))


################################################################################
# Apply the model to the test data.

prediction_data = read_data(prediction_file)
predictions = []
for avs, true_label in prediction_data:
    av_pairs = [x.split('=') for x in avs]
    scores = []
    for label in labels:
        score = parameters[label]
        for attr,val in av_pairs:
            score += parameters.get((attr,val,label), unknown_parameters[(attr,label)])
        scores.append((label,score))

    predictions.append(scores)

################################################################################
# Output the predictions on the prediction set.

for instance_scores in predictions:
    instance_scores.sort(key=itemgetter(1),reverse=True)
    total = sum([math.exp(x[1]) for x in instance_scores])
    if total > 0:
        instance_scores = [(x[0], math.exp(x[1])/total) for x in instance_scores]
    else: 
        instance_scores = [(x[0], 1.0/len(labels)) for x in instance_scores]

    output_file.write(" ".join([str(x[0]) + " " + str(x[1]) for x in instance_scores]) + "\n")
