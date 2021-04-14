import praw
import config
import os, json

with open("idioms.json") as f:
    idioms = json.load(f)

def login():
    print("Login in...")
    r = praw.Reddit(username=config.username,
                password=config.password,
                client_id=config.client_id,
                client_secret=config.client_secret,
                user_agent="lany13's idiom responder 1.0")
    print("Successful!")
    return r

def run(r, comments_seen):
    for comment in r.subreddit('test').comments(limit=25):
        for idiom in idioms:
            if idiom.lower().replace(",", "") in comment.body.lower().replace(",", "")\
                    and comment.id not in comments_seen and comment.author != r.user.me():
                comment.reply("You used an idiom!\n\n>{}\n\n{}".format(idiom, idioms[idiom].capitalize()))
                comments_seen.append(comment.id)
                with open("comments_seen.txt", "a") as f:
                    f.write(comment.id + "\n")
                print("Replied to comment", comment.id)

def get_seen_comments():
    if not os.path.isfile("comments_seen.txt"):
        comments_seen = []
    else:
        with open("comments_seen.txt", "r") as f:
            comments_seen = f.readlines()
            comments_seen = list(filter(None, comments_seen))
    return comments_seen

r = login()
comments_seen = get_seen_comments()
run(r, comments_seen)