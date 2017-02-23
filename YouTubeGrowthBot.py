import praw
import config


def bot_login():
    print("Logging in...")
    reddit = praw.Reddit(username=config.username,
                         password=config.password,
                         client_id=config.client_id,
                         client_secret=config.client_secret,
                         user_agent="YouTube_Growth Bot v0.1 (By /u/PythonBotTester)")
    print("Logged in")
    return reddit


def get_approved_posters(reddit):

    subreddit = reddit.subreddit('Subreddit Here')
    subreddit_comments = subreddit.comments(limit=1000)
    dictionary_of_posters = {}
    unique_posters = {}
    commentCount = 1
    duplicate_check = False
    unique_authors_file = open("unique_posters.txt", "w")

    print("Obtaining comments...")
    for comment in subreddit_comments:
        dictionary_of_posters[commentCount] = str(comment.author)
        for key, value in dictionary_of_posters.items():
            if value not in unique_posters.values():
                unique_posters[key] = value
        for key, value in unique_posters.items():
            if key >= 3:
                commentCount += 1
            if duplicate_check is not True:
                commentCount += 1
                print("Adding author to dictionary of posters...")
                unique_posters[commentCount] = str(comment.author)
                print("Author added to dictionary of posters.")
                if commentCount >= 3:
                    duplicate_check = True

    for x in unique_posters:
        unique_authors_file.write(str(unique_posters[x]) + '\n')

    total_comments = open("total_comments.txt", "w")
    total_comments.write(str(dictionary_of_posters))

    unique_authors_file.close()
    total_comments.close()

    unique_authors_file = open("unique_posters.txt", "r+")
    total_comments = open("total_comments.txt", "r")
    data = total_comments.read()
    approved_list = unique_authors_file.read().split('\n')
    print(approved_list)
    approved_posters = open("approved_posters.txt", "w")
    for username in approved_list:
        count = data.count(username)
        if(count >= 3):
            approved_posters.write(username + '\n')
        print("Count for " + username + " is " + str(count))

    approved_posters.close()
    unique_authors_file.close()
    total_comments.close()


def remove_unapproved_posts(reddit):
    subreddit = reddit.subreddit('Subreddit Here')
    posts = subreddit.hot(limit=None)
    for post in posts:
        if str(post.author) in open("approved_posters.txt").read():
            continue
        else:
            print("post title " + str(post))
            post.mod.remove()

reddit = bot_login()
get_approved_posters(reddit)
remove_unapproved_posts(reddit)
