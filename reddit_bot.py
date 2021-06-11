#!/usr/bin/python
from urllib.parse import quote_plus
import praw

QUESTIONS = ["what is", "who is", "what are"]
REPLY_TEMPLATE = "[Let me google that for you](https://lmgtfy.com/?q={})"
REPLY_MESSAGE = "Hello, you have summoned me!"

#Enter your correct Reddit information into the variable below
reddit = praw.Reddit(
    user_agent="Dummy Bot",
    client_id="wb5_poZESLKZ0Q",
    client_secret="OzbPjQyO4PHJfS5lPZM5FfnynACphA",
    username="BloodInTheWalter",
    password="Spidvagon01",)

numFound = 0

subreddit = reddit.subreddit('Anime') #any subreddit you want to monitor

bot_phrase = 'Hey, I like Anime!' #phrase that the bot replies with

keywords = {'Anime', 'Japanese cartoons', 'Naruto', 'Bleach'} #makes a set of keywords to find in subreddits

for submission in subreddit.hot(limit=10): #this views the top 10 posts in that subbreddit
    n_title = submission.title.lower() #makes the post title lowercase so we can compare our keywords with it.

    for i in keywords: #goes through our keywords

        if i in n_title: #if one of our keywords matches a title in the top 10 of the subreddit

            numFound = numFound + 1

            print('Bot replying to: ') #replies and outputs to the command line

            print("Title: ", submission.title)

            print("Text: ", submission.selftext)

            print("Score: ", submission.score)

            print("---------------------------------")

            print('Bot saying: ', bot_phrase)

            print()

            submission.reply(bot_phrase)

if numFound == 0:
    print()
    print("Sorry, didn't find any posts with those keywords, try again!")

def process_submission(submission):
    # Ignore titles with more than 10 words as they probably are not simple questions.
    if len(submission.title.split()) > 10:
        return
    normalized_title = submission.title.lower()
    for question_phrase in QUESTIONS:
        if question_phrase in normalized_title:
            url_title = quote_plus(submission.title)
            reply_text = REPLY_TEMPLATE.format(url_title)
            print(f"Replying to: {submission.title}")
            submission.reply(reply_text)
            # A reply has been made so do not attempt to match other phrases.
            break


def run_bot():
    print("Obtaining 25 comments...")
    for comment in subreddit.comments(skip_existing=True):
        if "Hey, Dummy Bot!".lower() in comment.body.lower() and comment.author != reddit.user.me():
            print('String summoning me has been found in comment {}',format(comment.id))
            comment.reply(REPLY_MESSAGE)
            print("Replied to comment " + comment.id)

for submission in subreddit.new(limit=10):
    process_submission(submission)
    run_bot()