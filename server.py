from flask import Flask, jsonify
from process_sentiment import Sentiment
from tweet_data_stream import TweetListener
from db import DB
import tweepy
import time
import json

app = Flask(__name__)
db = DB('northlondon','tweet_sentiments')

class TweetSentiment(object):

    def __init__(self, term, size):
        self.term = term
        self.size = size

    def get_tweets(self):
        print "getting stream"
        l = TweetListener(self.size)
        stream = tweepy.Stream(l.get_auth(), l)
        stream.filter(track=[self.term])
        return l.get_tweet_data()


    def get_sentiment(self, tweet_list):
        ps = Sentiment('jMLgHaogWBD7qwDYd9e31A41iibG76gvWcDWg6PehAs')    
        out = []
        for tweet in tweet_list:
            tmp = {}
            localtime = time.asctime( time.localtime(time.time()) )
            sentiment = ps.get_sentiment({"Text":tweet}) 
            #print "term: " + term
            tmp['term'] = self.term
            #print "tweet: "+tweet
            tmp['tweet'] = tweet 
            #print "sentiment:  ",sentiment + "\n\n"
            tmp['score'] = sentiment 
            tmp['date'] = localtime  
            out.append(tmp) 
        return out
        
    def get_result(self):
        
        tw = get_tweets()
        st = get_sentiment(tw)
        
        return str(st)
        
def run_tweet_sentiment(term, size):
    print "Initializing..."
    ts = TweetSentiment(term,size)
    print "Gathering Tweets..."
    result = ts.get_tweets()
    print "Processing sentiment..."
    sent = ts.get_sentiment(result)
    
    if db.add_many(sent) == True:
        print "Data insert complete"
    else:
        print "Data insert incomplete"
    
    return sent


def get_all_string(term):
    out_str = ""
    data = db.find({"term":term})
    for d in data:
        out_str += "<p>"+str(d)+"</p>"
        
    html_out = "<html><body>"+out_str+"</body></html>"
    return html_out

def get_all_list(term):
    out = []
    data = db.find({"term":term})
    for d in data:
        tmp = {}
        
        tmp['tweet'] = d['tweet']
        tmp['score'] = d['score']
        tmp['date'] = d['date']
        out.append(tmp)
    return out




""" ROUTES """

@app.route("/")
def hello():
    return "Hello world \n"


@app.route("/q/<term>")
def start_query(term):
    print "Doing jsonify"

    t = get_all_list(term)
    return jsonify(result=t)
    
@app.route("/s/<text>")
def tweet_search(text):
    print "Text recieved "+ text
    ts = run_tweet_sentiment(text, 10)
    allq = get_all_list(text)
    return jsonify(result=allq)   

if __name__ == "__main__":
    term = "arsenal"
    #dt = run_tweet_sentiment(term, 10)
    print "DONE!"
   # print get_all_list(term)
    app.run()
