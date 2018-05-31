#!/usr/bin/env python

import tweepy
from tweepy import TweepError

from secrets import consumer_key, consumer_secret, access_token, access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def get_user(username):
    try:
        return api.get_user(username)
    except TweepError:
        return None

print(get_user('yidcheng'))