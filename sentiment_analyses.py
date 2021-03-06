from tweepy.streaming import StreamListener #used to listen the tweets
from tweepy import OAuthHandler #used for authociation
from tweepy import Stream
from tweepy import API
from tweepy import Cursor

import tokens
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob


#This class will be using to get tweets from a particular client
class TwitterClient():

    def __init__(self,twitter_user=None):
        self.auth=Twitter_Auth().twitter_authenticator_app()
        self.twitter_client= API(self.auth)
        
        self.twitter_user=twitter_user

    def get_user_client_api(self):
        return self.twitter_client

    def get_twitter_timeline_user(self,tweet_num):
        tweets=[]
        for tweet in Cursor(self.twitter_client.user_timeline,id=self.twitter_user).items(tweet_num):
            tweets.append(tweet)
        return tweets
        
    def get_firend_list(self,num_friend):
        friend_list=[]
        for tweet in Cursor(self.twitter_client.friends,id=self.twitter_user).items(num_friend):
            friend_list.append(tweet)
        return(friend_list)

    def get_home_timeline_tweets(self,tweet_num):
        tweets=[]
        for tweet in Cursor(self.twitter_client.home_timeline,id=self.twitter_user).items(tweet_num):
            tweets.append(tweet)
        return(tweets)

#This is a seperate class for twitter authentication
class Twitter_Auth():

    def twitter_authenticator_app(self):
        auth=OAuthHandler(tokens.API_Token,tokens.API_Token_Secret)
        auth.set_access_token(tokens.Access_Token,tokens.Access_Token_Secret)
        return auth


 #This class is responsible for streaming and processing the tweets
class TwitterStreamer():

    def __init__(self):
        self.twitter_authenticator=Twitter_Auth()

    def stream_tweets(self,tweets_fillname,hash_tags):
        listener= TwitterListener(tweets_fillname)
        auth=self.twitter_authenticator.twitter_authenticator_app()

        stream= Stream(auth,listener)
        stream.filter(track=hash_tags)



#This class is a basic listener class listens and writes the data to StdOut
class TwitterListener(StreamListener):

    def __init__(self,tweets_fillname):
        self.tweets_fillname=tweets_fillname
    #will take and give us the data
    def on_data(self, data):
        try:
            print(data)
            with open(self.tweets_fillname,"a") as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" %str(e))
        return True
#will give us the status of error
    def on_error(self, status):
        if status==420:
            return False
        print(status)

#To analyze the tweets and to read them properly
class TweetAnalyzer():

    def clean_tweets(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def sentiment_analyses(self,tweet):
        Analysis=TextBlob(self.clean_tweets(tweet))

        if Analysis.sentiment.polarity > 0:
            return 1
        elif Analysis.sentiment.polarity== 0:
            return 0
        else:
            return -1

    def tweet_to_data(self,tweets):
        df= pd.DataFrame(data=[tweet.text for tweet in tweets],columns=["Texts"])
        df["id"]=np.array([tweet.id for tweet in tweets])
        df["date"]=np.array([tweet.created_at for tweet in tweets])
        df["len"]=np.array([len(tweet.text) for tweet in tweets])
        df["retweet_c"]=np.array([tweet.retweet_count for tweet in tweets])
        df["source"]=np.array([tweet.source for tweet in tweets])
        df["likes"]=np.array([tweet.favorite_count for tweet in tweets])
        return df

if __name__ == "__main__":

    user_client=TwitterClient()
    tweet_analyzer=TweetAnalyzer()

    api=user_client.get_user_client_api()
    tweets=api.user_timeline(screen_name="myogiadityanath",count=200)

    df = tweet_analyzer.tweet_to_data(tweets)
    df["Sentiments"]=np.array([tweet_analyzer.sentiment_analyses(tweet) for tweet in df["Texts"]])

    print(df.head(20))
   