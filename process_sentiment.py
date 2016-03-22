# -*- coding: utf-8 -*-

import urllib2
import urllib

import sys
import base64
import json 

class Sentiment(object):

    def __init__(self, access_key):
        self.credentials = base64.b64encode('AccountKey:' + access_key)
        self.base_url = 'https://api.datamarket.azure.com/data.ashx/amla/text-analytics/v1'
        self.headers = {'Content-Type':'application/json', 'Authorization':('Basic '+ self.credentials)}
        
    def get_sentiment(self, params):
    
        sentiment_url = self.base_url + '/GetSentiment?' + urllib.urlencode(params)
        req = urllib2.Request(sentiment_url, None, self.headers) 
        response = urllib2.urlopen(req)
        result = response.read()
        obj = json.loads(result)
        return (str(obj['Score'] *100))
           
        
    def get_key_phrases(self, params):
        # key phrases
        key_phrases_url = self.base_url + '/GetKeyPhrases?' + urllib.urlencode(params)
        req = urllib2.Request(key_phrases_url, None, self.headers) 
        response = urllib2.urlopen(req)
        result = response.read()
        obj = json.loads(result)
        return ('Key phrases: ' + ','.join(obj['KeyPhrases']))
        
