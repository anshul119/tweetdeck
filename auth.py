import oauth2 as oauth
import json
import requests
import os
import sys

CONSUMER_KEY = "FgwpSTfzWMTvQnBc61WSjdp19"
CONSUMER_SECRET = "V4lFdEjBfyh6SwQTRm9RvzPglKI72mJQt8rh1QJBc83QCaK4ay"
ACCESS_KEY = "313808280-9QiY09Kl0D9aj0SidVW6gqGCkmUY82H8cZv36hfP"
ACCESS_SECRET = "FY8LMvcDTR5EKhaGZfvGOhetb5RqCEY1ZixClQKYY7aBX"

class TwitterAPI():

       

        def __init__(self):
          self.ckey=CONSUMER_KEY
          self.csec=CONSUMER_SECRET
          self.akey=ACCESS_KEY
          self.asec=ACCESS_SECRET
          

	def Oauth_Twitter(self):
		self.consumer = oauth.Consumer(key=self.ckey, secret=self.csec)
		self.access_token = oauth.Token(key=self.akey, secret=self.asec)
		self.client = oauth.Client(self.consumer, self.access_token)


	def SearchHash(self,Uhash):
	        endpoint = "https://api.twitter.com/1.1/search/tweets.json?q=#"+Uhash+"&src=typd"
		print endpoint
		self.response, self.data = self.client.request(endpoint)
		self.tweets = json.loads(self.data)
		print self.tweets


