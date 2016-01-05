# -*- coding: utf-8 -*-
import tweepy
from emoji_data.emoticon_reader import emoji_filter

from learner import sentimentLearner
from jubatus.classifier.client import Classifier

from requests.packages.urllib3.exceptions import ProtocolError
from config import *

#Jubatus
host = '127.0.0.1'
port = 9199
name = 'sentimentModel'

happy_emoticons = emoji_filter(100, True, 0.49)
sad_emoticons = emoji_filter(100, False, -0.1)
emoticon_list = happy_emoticons + sad_emoticons

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def __init__(self,learner):
        super(MyStreamListener,self).__init__()
        self.learner = learner


    def on_status(self, status):
        tweet = status.text
        self.learner.trainTweet(tweet)

if __name__ == '__main__':

    client = Classifier(host, port, name)
    # client.load(name)
    learner = sentimentLearner(client, happy_emoticons, sad_emoticons)

    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    myStreamListener = MyStreamListener(learner)
    myStream = tweepy.Stream(auth = auth, listener=myStreamListener)

    while True:
        try:
        #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
            myStream.filter(track= emoticon_list,  languages = ["en"])
        except ProtocolError:
            continue

