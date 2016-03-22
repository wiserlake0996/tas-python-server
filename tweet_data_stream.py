import tweepy
import json
from timer import CusTimer as ct

# This is the listener, resposible for receiving data
class TweetListener(tweepy.StreamListener):
  
    def __init__(self,no_of_tweets):
        super(TweetListener, self).__init__()

        self.consumer_key="12qKBTDob4kE1Es3NydxEuKuu"
        self.consumer_secret="eTwRZG1djhk1gKPho9jDS6ossoSJPdofA6FeeMQq2KWQhpsEhw"
        self.access_token="59562463-WK8SUefvgczxch9PLvS3KawnDJvevDqWcnobQMJXS"
        self.access_token_secret="kLjks5X0q7MF1DfSEmeQ6sH8wWDyqFpE0WqcFwlcStiGe"        
        
        self.no_of_tweets = no_of_tweets
        self.tweet_count = 0
        self.tweet_list = []
        self.tweet_dict = []
        self.tweet_string = ""
        self.currtime = 0
        
        
    def get_auth(self):    
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        return auth

    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data) 
        
        tmp = dict()

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        self.tweet_list.append('@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')))
        
        tmp['user'] = decoded['user']['screen_name']
        tmp['text'] = decoded['text'].encode('ascii', 'ignore')
        
        self.tweet_dict.append(tmp)
        
        self.tweet_string += decoded['text'].encode('ascii', 'ignore') + "\n"
        
        self.tweet_count += 1
        
                
        if(self.tweet_count < self.no_of_tweets):
            return True
        else:
            print "Stopping twitter stream"

            return False
        

    def on_error(self, status):
        print status
        
    def get_tweet_data(self):
        return self.tweet_list
