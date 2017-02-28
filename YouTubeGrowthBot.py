import praw
import config
import json


def bot_login():
    print("Logging in...")
    reddit = praw.Reddit(username=config.username,
                         password=config.password,
                         client_id=config.client_id,
                         client_secret=config.client_secret,
                         user_agent="YouTube_Growth Bot v1.0 (By /u/PythonBotTester)")
    print("Logged in")
    return reddit


def delete_unapproved_posts(reddit):

    subreddit = reddit.subreddit('YouTube_Growth')
    subreddit_comments = subreddit.comments(limit=None)
    dictionary_of_posters = {}
    approved_authors = []
    json_dump = {'Comment Count': dictionary_of_posters, 'Approved Posters': approved_authors}

    print("Obtaining comments...")
    for comment in subreddit_comments:
        try:
            dictionary_of_posters[str(comment.author)] += 1
        except KeyError:
            dictionary_of_posters[str(comment.author)] = 1

    for username, comment_count in dictionary_of_posters.items():
        if comment_count >= 3:
            approved_authors.append(username)
    with open("json_dump.json", 'wb') as outfile:
        json.dump(json_dump, outfile)

    posts = subreddit.hot(limit=None)
    for post in posts:
        if str(post.author) in json_dump["Approved Posters"]:
            continue
        else:
            post.mod.remove()

    print("Unapproved posts have been removed.")

reddit = bot_login()
delete_unapproved_posts(reddit)