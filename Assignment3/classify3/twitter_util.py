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

NO_LABEL = "no_label"

class Tweet:

    def __init__(self):
        pass

    @classmethod
    def fromXmlElement (cls, itemEl):
        """Initialize an HcrTweet using an XML element."""
        obj = cls()
        obj.tweetid  = itemEl.get("tweetid")
        obj.userid   = itemEl.get("userid")
        obj.username = itemEl.get("username", "name_missing")
        obj.target   = itemEl.get("target", "general")
        obj.label    = itemEl.get("label", NO_LABEL)
        obj.content  = list(itemEl)[0].text

        return obj

    @classmethod
    def fromValues (cls, tweetid, userid, username, target, label, content):
        """Initialize a Tweet from raw values."""
        obj = cls()
        obj.tweetid  = tweetid
        obj.userid   = userid
        obj.username = username
        obj.target   = target
        obj.label    = label
        obj.content  = content
        return obj

    def to_string (self):
        return self.tweetid + " : " + self.username + \
            " (" + self.target + "," + self.label + ") " + self.content 

    def copy (self):
        return Tweet.fromValues(self.tweetid, self.userid, self.username, \
                                self.target, self.label, self.content)

def convert_posneg_to_subjective (tweetset):
    for tweet in tweetset:
        if tweet.label == "positive" or tweet.label == "negative":
            tweet.label = "subjective"
    return tweetset

def scoreForLabel (eval_labels, gold_labels, label):
    num_correct = sum([e==g and e==label for e,g in zip(eval_labels,gold_labels)])
    num_predicted = eval_labels.count(label)
    num_gold = gold_labels.count(label)
    precision = num_correct/num_predicted * 100.0 if num_predicted != 0 else 0.0
    recall = num_correct/num_gold * 100.0
    fscore = 2*precision*recall/(precision+recall) if precision+recall != 0 else 0.0
    return (precision,recall,fscore,label)

def scorePredictions (eval_tweets, gold_tweets):
    eval_labels = [x.label for x in eval_tweets]
    gold_labels = [x.label for x in gold_tweets]
    label_set = set(gold_labels)

    # Get overall accuracy: for each tweet, was the system correct or incorrect?
    correctness_vector = [e==g for e,g in zip(eval_labels,gold_labels)]
    accuracy = sum(correctness_vector)/len(gold_tweets) * 100.0

    # Get label-level results
    results = [scoreForLabel(eval_labels,gold_labels,label) for label in sorted(label_set)]

    return (accuracy, results, correctness_vector)
