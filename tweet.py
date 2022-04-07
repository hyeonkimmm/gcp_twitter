import tweepy
import json
from google.cloud import pubsub_v1
from google.oauth2 import service_account
key_path = "data/info/crypto-gantry-346511-2776d297279c.json"
credentials = service_account.Credentials.from_service_account_file(
 key_path,
 scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
client = pubsub_v1.PublisherClient(credentials=credentials)

# 파라미터 : 프로젝트id, 토픽 이름
topic_path = client.topic_path('crypto-gantry-346511', 'tweets')

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
        tweet = json.dumps({'id': status.id, 'created_at': status.created_at, 'text': status.text}, default=str)
        client.publish(topic_path, data=tweet.encode('utf-8'))
        
    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False


stream_listener = SimpleStreamListener()

auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)

twitterStream = tweepy.Stream(auth, stream_listener)
twitterStream.filter(track=['data'])

