# -*- coding: utf-8 -*-
import sys,json

from jubatus.classifier.client import Classifier
from jubatus.classifier.types import LabeledDatum
from jubatus.common import Datum

from tagger import CMUTweetTagger

from nltk.corpus import stopwords
from nltk.stem.porter import *

filter_tags = ['N', '^', 'V', 'A', 'R', '!', '#', 'E']
not_stem_tags = ['^', '!', '#', 'E']

# negation_cues = ["not", "never", ""]

class sentimentLearner():
    def __init__(self, model, happy_emoticons, sad_emoticons):
        self.model = model
        self.happy_emoticons = happy_emoticons
        self.sad_emoticons = sad_emoticons
        self.all_emoticons = map(lambda x:x.encode('utf-8') ,self.happy_emoticons + self.sad_emoticons)

        self.stop = [word.encode('utf-8') for word in stopwords.words('english')]

        self.stemmer = PorterStemmer()


    #guess the label based on emoticon, train it if it can guess
    #return boolean indicates whether it can be trained or not...
    def trainTweet(self, tweet):
        label = self.label(tweet)
        if label:
            tweet = self.processTweet(tweet)
            print tweet
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
        if any(emoticon in tweet for emoticon in self.happy_emoticons) and any(emoticon in tweet for emoticon in self.sad_emoticons):
            return ""
        elif any(emoticon in tweet for emoticon in self.happy_emoticons):
            return "happy"
        elif any(emoticon in tweet for emoticon in self.sad_emoticons):
            return "sad"
        return ""

    def processTweet(self, tweet):
        #tag the text
        analyse = CMUTweetTagger.runtagger_parse([tweet])
        analyse = analyse[0]

        #only return these match the tag and not the stop words
        filtered = filter(lambda x: (x[1] in filter_tags or x[0] in self.all_emoticons) and (x[0] not in self.stop), analyse)

        #do not stem the emoticon
        words = []
        for word in filtered:
            if (word[1] in not_stem_tags or word[0] in self.all_emoticons):
                words.append(word[0])
            else:
                #for all sorts of reason... might not able to stem the word...
                try:
                    words.append( self.stemmer.stem(word[0].lower()).encode("utf-8") )
                except:
                    # words.append(word[0])
                    continue

        return  " ".join(words).decode('utf-8')

    def classify(self, tweet):
        tweet = self.processTweet(tweet)
        datum = Datum({"tweet": tweet})
        print self.model.classify([datum])