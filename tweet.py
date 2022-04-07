import tweepy
import json
_PATH = 'data/info/tweet.json'
with open(_PATH, "r", encoding='utf-8-sig') as json_file:
    tweet_info = json.load(json_file)
    twitter_api_key = tweet_info['API_Key']
    twitter_api_secret_key = tweet_info['API_Key_Secret']
    twitter_access_token = tweet_info['Access_Token']
    twitter_access_token_secret = tweet_info['Access_Token_Secret']

class SimpleStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status)

stream_listener = SimpleStreamListener()
auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
twitterStream = tweepy.Stream(auth, stream_listener)
twitterStream.filter(track=['data'])

