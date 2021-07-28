import os

import tweepy
import re
import os
from PIL import Image, ImageDraw, ImageFont
from morse import morse_dict

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
SECRET_ACCESS_TOKEN = os.environ["SECRET_ACCESS_TOKEN"]

auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)

api = tweepy.API(auth)

mentions = api.mentions_timeline()

message = ""
# result_message = ""

# loop through mentions
for tweet in mentions:

    message = tweet.text
    message = message.lower()
    message_list = re.split(r'(\s+)', message)

    # print(message_list)

    # loop through the words in the tweet
    for word in message_list:
        # find the tag in the message and remove it
        if word[0] == "@":
            if message_list[message_list.index(word) + 1] == " ":
                message_list.pop(message_list.index(word) + 1)
                print(message_list)
            message_list.remove(word)

    # loop through the words in the tweet (again)
    result_message = ""
    for word in message_list:
        # loop through the letters in each word in order to convert them into morse code
        for letters in word:
            print(morse_dict[letters], end=" ")

# TODO convert text to image
# TODO Set environment variables for API keys
# TODO Creat git repo and post to GitHub
print("\nOriginal message: ", message)
