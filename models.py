from tweepy import OAuthHandler,StreamListener,Stream,API,Cursor
import sqlite3
import json
import re
import time
import datetime
import math
from random import sample
from app import *
        
class TweetDatabase (object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()

    def create(self):
        try:
            self.c.execute('''CREATE TABLE tweets
                                    ( id int not null unique,
                                    text text,
                                    url text,
                                    created_at text,
                                    retweet_count int,
                                    screen_name text,
                                    profile_image_url text,
                                    followers_count int);''')
            self.conn.commit()
            return True
        except sqlite3.OperationalError:
            return False

    def load(self):
        return self.c.execute('''select * from tweets;''')

    def save(self, data):
        self.create()
        self.c.executemany('''INSERT OR REPLACE INTO tweets 
                    VALUES (?,?,?,?,?,?,?,?)''', data)
        self.conn.commit()
        return True

    def purge(self):
        self.c.execute('''
            delete from tweets
            where datetime(created_at) < date('now','-8 day');
            ''')
        self.c.execute('vacuum;')
        self.conn.commit()
        return True
        
        
class FilteredTweets (object):
    def __init__(self):
        self.filtered_tweets = []
        self.db = TweetDatabase('tweets.sqlite')
        self.tweets = self.db.load()
        for tweet in self.tweets:
            id, text, url, created_at, retweet_count, screen_name, profile_image_url,\
                    followers_count = tweet
            score = self.build_score(retweet_count, followers_count)
            self.filtered_tweets.append(
                    {
                    'id': id, 
                    'text': text, 
                    'url': url, 
                    'created_at': created_at,
                    'retweet_count': retweet_count, 
                    'screen_name': screen_name, 
                    'profile_image_url': profile_image_url,
                    'followers_count': followers_count, 
                    'score': score
                    })
            self.filtered_tweets = sorted(self.filtered_tweets, key=lambda 
                    tup: tup['score'], reverse=True)


    def build_score(self, retweet_count, followers_count):
        retweet_count -= 1
        if retweet_count > 2:
            retweet_score = pow(retweet_count, 1.5)
            raw_score = (retweet_score / followers_count)*100000
            score = round(math.log(raw_score, 1.09))
        else:
            score = 0
        return int(score)

    def load_by_date(self, close, far):
        self.date_filtered_tweets=[]
        counter = 0
        for tweet in self.filtered_tweets:
            self.created_at_object = datetime.datetime.strptime(
                    tweet['created_at'], '%Y-%m-%dT%H:%M:%S')
            if (self.created_at_object > self.build_date(far) 
                    and self.created_at_object < self.build_date(close)
                    and counter < 40):
                self.date_filtered_tweets.append(tweet)
                counter += 1
        return self.date_filtered_tweets

    def build_date(self, day_delta):
        filter_date = (
                datetime.datetime.today() - 
                datetime.timedelta(days=day_delta)).replace(
                        hour=0, minute=0, second=0, microsecond=0)
        return filter_date

#Css color names for random color 
       
CSS_COLOR_NAMES = ["AliceBlue","AntiqueWhite","Aqua","Aquamarine","Azure","Beige","Bisque","Black","BlanchedAlmond","Blue",
"BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan",
"DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGrey","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","Darkorange",
"DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkSlateGrey","DarkTurquoise","DarkViolet",
"DeepPink","DeepSkyBlue","DimGray","DimGrey","DodgerBlue","FireBrick","FloralWhite","ForestGreen","Fuchsia","Gainsboro","GhostWhite",
"Gold","GoldenRod","Gray","Grey","Green","GreenYellow","HoneyDew","HotPink","IndianRed","Indigo","Ivory","Khaki","Lavender",
"LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGrey",
"LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray","LightSlateGrey","LightSteelBlue","LightYellow",
"Lime","LimeGreen","Linen","Magenta","Maroon"]
