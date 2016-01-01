from tweepy import OAuthHandler,StreamListener,Stream,API,Cursor
import sqlite3
import json
import re
import time
import datetime
import math
from random import sample
from app import *

class Tweets (object):
    def __init__(self):
    
		auth = OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
		auth.set_access_token(app.config['ACCESS_TOKEN'], app.config['ACCESS_TOKEN_SECRET'])
		api = API(auth,wait_on_rate_limit=True) 		
		self.db = 'tweets.sqlite'
		self.tweets = []
		#Get worldwide trend topics
		k = api.trends_place(1)
		trends = [i['name'] for i in k[0]['trends']]
		#random_numbers = sample(xrange(len(trends)-1),10) # create 10 random numbers for random trends search
		""" This is the my home_timeline and I'll categorize from my twitter account to more true result """ 
		for tweet in api.home_timeline(count=200, include_rts=0): 
			try:
				url = tweet.entities['urls'][0]['expanded_url']
			except IndexError:
				url = False
			if (url is not False):
				self.tweets.append((
				        tweet.id_str,
				        self.extract_urls(tweet.text),
				        url,
				        str(tweet.created_at).replace(' ', 'T'),
				        tweet.retweet_count,
				        tweet.user.screen_name,
				        tweet.user.profile_image_url.replace("_normal",""),
				        tweet.user.followers_count
				        ))

		for i in range(30):
			for tweet in Cursor(api.search,q=trends[i],result_type="popular").items(19):
				try:
				    url = tweet.entities['urls'][0]['expanded_url']
				except:
				    url = False

				if (url is not False):
				    self.tweets.append((
				            tweet.id_str,
				            self.extract_urls(tweet.text),
				            url,
				            str(tweet.created_at).replace(' ', 'T'),
				            tweet.retweet_count,
				            tweet.user.screen_name,
				            tweet.user.profile_image_url.replace("_normal",""),
				            tweet.user.followers_count
				            ))                                   
                                           

    def save(self):
        tdb = TweetDatabase(self.db)
        tdb.save(self.tweets)
        tdb.purge()

    def extract_urls(self, text):
        text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
                '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '',
                text).strip()
        text = re.sub('\:$', '', text)
        return text
        
if __name__ == '__main__':
	remote_tweets = Tweets()
	remote_tweets.save()
