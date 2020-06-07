from tweepy.streaming import StreamListener #used to listen the tweets
from tweepy import OAuthHandler #used for authociation
from tweepy import Stream
from tweepy import API
from tweepy import Cursor

import tokens


#This class will be using to get tweets from a particular client

class TwitterClient():

    def __init__(self,twitter_user):
        self.auth=Twitter_Auth().twitter_authenticator_app()
        self.twitter_client= API(self.auth)
        
        self.twitter_user=twitter_user

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

if __name__ == "__main__":

    hash_tags=["donald trump","hillary clinton","barack obama"]
    tweets_fillname="tweets.txt"

    twitter_client=TwitterClient("gvanrossum")
    print(twitter_client.get_firend_list(1))
    #tweeter_streamer=TwitterStreamer()
    #tweeter_streamer.stream_tweets(tweets_fillname,hash_tags)
    