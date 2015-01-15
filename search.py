import oauth2 as oauth
import json
import requests
import os
import sys
from flask import Flask,jsonify
from flask.ext.cors import CORS
from flask import render_template
from flask import request, session, g, redirect, url_for, abort, \
      flash, _app_ctx_stack

CONSUMER_KEY = "bRQ8lijzeN6cweEfi7tPn2R2X"
CONSUMER_SECRET = "W940lRsPkCKJKpNGEiRKjYa4BHVMWC7zgPP4pLY8tYuyllwXRm"
ACCESS_KEY = "313808280-9QiY09Kl0D9aj0SidVW6gqGCkmUY82H8cZv36hfP"
ACCESS_SECRET = "FY8LMvcDTR5EKhaGZfvGOhetb5RqCEY1ZixClQKYY7aBX"

tweets={}
approved_tweets={}
blocked_tweets={}
backend_tweets={}
new_tweets={}
new_approved={}
app = Flask(__name__,static_url_path='/static')

class TwitterAPI():
       
	def Oauth_Twitter(self):
                self.consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
		self.access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
		self.client = oauth.Client(self.consumer, self.access_token)

	def SearchHash(self,Uhash,frm):
                global backend_tweets,new_tweets,tweets
                endpoint = "https://api.twitter.com/1.1/search/tweets.json?q=%23"+Uhash+"&src=typd&include_entities=False&result_type=recent"
		print "EndPoint to be queried, Wait\n"+endpoint
		self.response, self.data = self.client.request(endpoint)
		self.tweets_J = json.loads(self.data)
                
                for tweet in self.tweets_J['statuses']:
                      if (tweets.has_key(tweet['id_str'])==False):
                           tweets[tweet['id_str']]= "https://twitter.com/"+tweet['user']['screen_name']+"/status/"+tweet['id_str']
                           if frm=="backend":
                             new_tweets[tweet['id_str']]= "https://twitter.com/"+tweet['user']['screen_name']+"/status/"+tweet['id_str'] 
                if frm=="index":
                  backend_tweets = tweets

Search = TwitterAPI()

@app.route('/')
def index():
  Search.SearchHash("techieb","backend")   
  return jsonify(tweets)


@app.route('/back')
def back():
  global backend_tweets
  return jsonify(backend_tweets)

@app.route('/update')
def update():
  global new_tweets,backend_tweets
  new_tweets.clear()
  Search.SearchHash("techieb","backend")
  backend_tweets = dict(backend_tweets.items()+new_tweets.items())
  return jsonify(new_tweets)


@app.route('/approved')
def approve():
  global approved_tweets
  return jsonify(approved_tweets)


@app.route('/blocked')
def blocked():
  global blocked_tweets
  return jsonify(blocked_tweets)

@app.route('/user')
def user():
  return render_template("index.html")  

@app.route('/backend')
def backend():
  return render_template("backend.html")  

@app.route('/backend_approved')
def backend_approved():
  return render_template("approved.html")  

@app.route('/backend_blocked')
def backend_blocked():
  return render_template("blocked.html")  

@app.route('/sensor',methods=['GET','POST'])
def sensor():
    global tweets,approved_tweets,new_tweets,blocked_tweets,backend_tweets,new_approved

    data = json.loads(request.data)
    diff=[]
    if(len(approved_tweets)> len(data)):
     diff = list(set(approved_tweets.keys()) - set(data))
    else:
     diff = list(set(data) - set(approved_tweets.keys()))
    for dif in diff:
        if(approved_tweets.has_key(dif)):
            print approved_tweets[dif]
            del approved_tweets[dif]
 
    for at in data:
        approved_tweets[at]=tweets[at]

    backend_tweets=approved_tweets
   
    keys_b = approved_tweets.keys()
    for key in tweets.keys():
     if not key in keys_b:
         blocked_tweets[key]=tweets[key]
  
    return jsonify(approved_tweets)

@app.route('/sensor_a',methods=['GET','POST'])
def sensora():
    global tweets,approved_tweets,new_tweets,blocked_tweets,backend_tweets
    
    data = json.loads(request.data)
    for at in data:
        blocked_tweets[at]=tweets[at]
  
    for at in data:
        del approved_tweets[at]
        print at

    backend_tweets=approved_tweets
    return jsonify(approved_tweets)
@app.route('/unsensor',methods=['GET','POST'])
def unsensor():
    global tweets,approved_tweets,new_tweets,blocked_tweets,backend_tweets
    
    data = json.loads(request.data)
    for at in data:
        approved_tweets[at]=tweets[at]
  
    for at in data:
        del blocked_tweets[at]
        print at

    backend_tweets=approved_tweets
    return jsonify(blocked_tweets)
if __name__=="__main__":
   Search.Oauth_Twitter()
   Search.SearchHash("techieb","index")  
   app.run(host="0.0.0.0",port=int(8080),debug=True)
