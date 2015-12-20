# -*- coding: utf-8 -*-
import sys,json

from jubatus.classifier.client import Classifier
from jubatus.classifier.types import LabeledDatum
from jubatus.common import Datum

# happy_emoticons = [u'☺', u'☻']
# sad_emoticons = [u'☹']

class sentimentLearner():
    def __init__(self, model, happy_emoticons, sad_emoticons):
        self.model = model
        self.happy_emoticons = happy_emoticons
        self.sad_emoticons = sad_emoticons


    #guess the label based on emoticon, train it if it can guess
    #return boolean indicates whether it can be trained or not...
    def trainTweet(self, tweet):
        label = self.label(tweet)
        if label:
            datum = Datum({"tweet": tweet})
            labeldatum = LabeledDatum(label, datum)
            self.model.train([labeldatum])

            all_emoticons = self.happy_emoticons + self.sad_emoticons
            for emoticon in all_emoticons:
                tweet = tweet.replace(emoticon, "")
            
            datum = Datum({"tweet": tweet})
            labeldatum = LabeledDatum(label, datum)
            self.model.train([labeldatum])

            print self.model.save("sentimentModel")
            return True
        return False


    #label the tweet based on emoticon
    def label(self, tweet):

        # if ":)" in tweet and ":(" in tweet:
        #   return ""
        # elif ":)" in tweet:
        #   return "happy"
        # elif ":(" in tweet:
        #   return "sad"
        # return ""

        if any(emoticon in tweet for emoticon in self.happy_emoticons) and any(emoticon in tweet for emoticon in self.sad_emoticons):
            return ""
        elif any(emoticon in tweet for emoticon in self.happy_emoticons):
            return "happy"
        elif any(emoticon in tweet for emoticon in self.sad_emoticons):
            return "sad"
        return ""
