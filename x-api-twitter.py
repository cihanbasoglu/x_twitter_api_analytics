from requests_oauthlib import OAuth1Session
import pandas as pd

consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

twitter = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret
)

user_fields = [
    "affiliation", "connection_status", "created_at", 
    "description", "entities", "id", "is_identity_verified", "location", 
    "most_recent_tweet_id", "name", "parody", "pinned_tweet_id", 
    "profile_banner_url", "profile_image_url", "protected", "public_metrics", 
    "receives_your_dm", "subscription", "subscription_type", "url", 
    "username", "verified", "verified_followers_count", "verified_type", 
    "withheld"
]

tweet_fields = [
    "attachments", "author_id", "card_uri", "context_annotations",
    "conversation_id", "created_at", "entities", "geo", "id",
    "in_reply_to_user_id", "lang", "public_metrics", "referenced_tweets",
    "reply_settings", "source", "text", "non_public_metrics", "organic_metrics"
]

params = {
    "tweet.fields": ",".join(tweet_fields),
    "user.fields": ",".join(user_fields),
    "expansions": "affiliation.user_id,most_recent_tweet_id,pinned_tweet_id"
}

url = "https://api.twitter.com/2/users/me"
response = twitter.get(url, params=params)

response_json = response.json()

user_df = pd.json_normalize(response_json['data'])

tweets_df = pd.DataFrame()
if 'includes' in response_json and 'tweets' in response_json['includes']:
    tweets_df = pd.json_normalize(response_json['includes']['tweets'])
    tweets_df['user_id'] = response_json['data']['id']

tweets_df.to_csv('twitter_test_tweets.csv', index=False)
user_df.to_csv('twitter_test_users.csv', index=False)