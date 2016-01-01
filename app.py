import os
from random import sample
from flask import Flask,render_template,url_for,redirect,abort,session,request
from models import *

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/',methods=["GET"])
def home():
	tweets = FilteredTweets()
	datas  = [tweets.filtered_tweets[i] for i in range(len(tweets.filtered_tweets)) ]
	return render_template("presentation.html",datas   = datas,
											   numbers = range( len(tweets.filtered_tweets)),
											   colors  = CSS_COLOR_NAMES )


if __name__ == '__main__':
	app.run(debug=True)




