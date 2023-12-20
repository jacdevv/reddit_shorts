import praw
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

CLIENT_KEY = os.getenv("CLIENT_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

def fetch_reddit_data(subreddit):
    print("Fetching Reddit data...")
    reddit = praw.Reddit(client_id=CLIENT_KEY, client_secret=SECRET_KEY, user_agent='userAgent')
    posts = reddit.subreddit(subreddit).hot(limit=1)
    
    for post in posts:
        post.comments.replace_more(limit=0)
        filtered_comments = filter(lambda comment: len(comment.body.split()) >= 100, post.comments)
        comment = next(filtered_comments, None)
        if comment:
            return post.title, comment.body
    return None, None
