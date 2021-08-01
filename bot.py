import os
import textwrap

import tweepy
import re
from PIL import Image, ImageDraw, ImageFont
from morse import morse_dict
import logging
from config import create_api
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_mentions(api, keywords, since_id):
    logger.info("Checking mentions...")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        message = tweet.text
        message = message.lower()
        # print("\nOriginal message: ", message)
        message_list = re.split(r'(\s+)', message)

        # print(message_list)

        # loop through the words in the tweet
        for word in message_list:
            # find the tag in the message and remove it
            if word[0] == "@":
                if message_list[message_list.index(word) + 1] == " ":
                    message_list.pop(message_list.index(word) + 1)
                    # print(message_list)
                message_list.remove(word)

        # loop through the words in the tweet (again)
        result_message = ""
        for word in message_list:
            # loop through the letters in each word in order to convert them into morse code
            for letters in word:
                result_message = result_message + morse_dict[letters] + " "

        # print("Result message: " + result_message)

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

        # this loops through the message and does text wrapping
        for line in textwrap.wrap(result_message, width=40):
            draw.text((margin, offset), line, font=font, fill="white")
            offset += font.getsize(line)[1]

        img.save("morse_img.png")
        new_since_id = max(tweet.id, new_since_id)

        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Replying to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()

        api.update_with_media("morse_img.png", in_reply_to_status_id=tweet.id)

    return new_since_id


def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["@MorseTranslator"], since_id)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
