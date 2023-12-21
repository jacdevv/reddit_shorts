import praw
import os
import random
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

CLIENT_KEY = os.getenv("CLIENT_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

def fetch_reddit_data(subreddit, mode='comment'):
    subreddit = subreddit.replace(" ", "")  # Remove whitespace from subreddit argument
    mode = mode.replace(" ", "")  # Remove whitespace from mode argument

    print("Fetching Reddit data...")
    reddit = praw.Reddit(client_id=CLIENT_KEY, client_secret=SECRET_KEY, user_agent='userAgent')
    posts = reddit.subreddit(subreddit).hot(limit=50)  # Increase limit to 50

    skip = random.randint(0, 49)  # Generate a random number between 0 and 49
    for _ in range(skip):  # Skip a random number of posts
        next(posts)

    max_attempts = 100
    attempt = 0
    
    post = next(posts, None)  # Get the next post
    while post and attempt < max_attempts:
        attempt += 1
        if mode == 'post':
            word_count = len(post.selftext.split())
            if word_count > 250 and word_count < 300:
                return post.selftext
            elif word_count <= 250 or word_count > 300:
                post = next(posts, None)  # Find another post if the current post doesn't have over 250 words
                continue
        else:
            post.comments.replace_more(limit=0)
            filtered_comments = filter(lambda comment: len(comment.body.split()) >= 100, post.comments)
            comment = next(filtered_comments, None)
            if comment:
                return post.title, comment.body

    raise Exception("No suitable post found after {} attempts".format(max_attempts))