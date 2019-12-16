# changed language interpreter
import json
import os
import time
import tkinter
import praw  # reddit api
import requests
import tweepy  # twitter api
from pyshorturl import Googl, ShortenerServiceError

# twitter consumer and access keys
consumer_key = '***************'
consumer_secret = ''***************'
access_token = ''***************-'***************'
access_token_secret = ''***************'

# authentication token
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# user created
user = api.me()
print(user.name)

# this will fetch images from eyebleach

#still need to change the access keys for the actual 'sans-sad' account 
def setup_connection_reddit(eyebleach):
    print("sans-sad setting up connection with reddit")
    #using my personal account
    ram = praw.Reddit(client_id=''***************', client_secret=''***************',
                      password='****', username='*****', user_agent='my_bot')
    eyebleach = ram.subreddit("eyebleach")
    # basically anytime you see an example with something like get_x, remove the get_ part.
    return eyebleach

# twitter bot part


def tweet_er(subreddit_info):
    post_dict = {}
    post_ids = []
    print("sans-sad getting posts from Reddit")

    for submission in subreddit_info.hot(limit=1):
        post_dict[strip_title(submission.title)] = submission.url
        post_ids.append(submission.id)

    print("sans-sad generating short links")
    mini_post_dict = {}
    for post in post_dict:
        post_title = post
        post_link = post_dict[post]
        service = Googl()
        try: 
            short_link = service.shorten_url(post_link)
        except:
            print("error")
    return mini_post_dict, post_ids


# this part is supposed to shorten links
# def shorten(url):
#     headers = {'content-type' : 'applications/json'}
#     payload = {"longURL": url}
#     url = "https://www.googleapis.com/urlshortener/v1/url"
#     r = requests.post(url, data=json.dumps(payload), headers=headers)
#     print("This is where the error starts")
#     link = json.loads(r.text)['id']
#     print("SUCCESS!")
#     return link

# truncates titles to tweet length
def strip_title(title):
    if len(title) < 250:
        return title
    else:
        return title[:249] + "..."

# post ids


def add_id_to_file(id):
    with open('posted_posts.txt', 'a') as file:
        file.write(str(id) + "\n")


def duplicate_check(id):
    found = 0
    with open('posted_posts.txt', 'r') as file:
        for line in file:
            if id in line:
                found = 1
    return found

# prevent duplicate posts


def tweeter(post_dict, post_ids):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    for post, post_id in zip(post_dict, post_ids):
        found = duplicate_check(post_id)
        if found == 0:
            print("sans-sad posting link on twitter")
            print +" "+post_dict[post]+" #wala #python #bot"
            api.update_status(post+" "+post_dict[post]+" #wala #python #bot")
            add_id_to_file(post_id)
            time.sleep(30)
        else:
            print("sans-sad does NOT repeat posts")

# main function


def main():
    subreddit = setup_connection_reddit('python')
    post_dict, post_ids = tweet_er(subreddit)
    tweeter(post_dict, post_ids)


#imported or executed
if __name__ == '__main__':
    main()


