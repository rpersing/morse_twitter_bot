import os
import textwrap

import tweepy
import re
import os
from PIL import Image, ImageDraw, ImageFont
from morse import morse_dict
from textwrap import wrap

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
SECRET_ACCESS_TOKEN = os.environ["SECRET_ACCESS_TOKEN"]

auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)

api = tweepy.API(auth)

mentions = api.mentions_timeline()

message = ""
result_message = ""

# loop through mentions
for tweet in mentions:

    message = tweet.text
    message = message.lower()
    print("\nOriginal message: ", message)
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
    for word in message_list:
        # loop through the letters in each word in order to convert them into morse code
        for letters in word:
            result_message = result_message + morse_dict[letters] + " "

print("Result message: " + result_message)

img = Image.new("RGBA", (400, 600), color="black")

margin = offset = 40
fontsize = 25
img_fraction = 0.5

font = ImageFont.truetype("arial.ttf", fontsize)

while font.getsize(result_message)[0] < img_fraction * img.size[0]:
    fontsize += 1
    font = ImageFont.load_default()

fontsize -= 1
font = ImageFont.truetype("arial.ttf", fontsize)

draw = ImageDraw.Draw(img)

for line in textwrap.wrap(result_message, width=40):
    draw.text((margin, offset), line, font=font, fill="white")
    offset += font.getsize(line)[1]

img.save("morse_img.png")




