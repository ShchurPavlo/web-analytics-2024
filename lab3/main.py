import praw
import pandas as pd
import csv
from datetime import datetime, timezone


def Autorization():
    id = input("Enter client id: ")
    secret = input("Enter client secret: ")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    try:
        client=praw.Reddit(client_id=id,client_secret=secret,user_agent=user_agent)
        print("Authentication successful!")

    except Exception as e:
        print("Authentication failed:", e)
        exit()
    return client


def Parse(client,target):
    result = []
    for submission in client.redditor(target).submissions.new(limit=2000):
        if submission.is_self and submission.selftext:
            post_text = submission.selftext
        else:
            post_text = None
            result.append({
                'id': submission.id,
                'author': submission.author,
                'title': submission.title,
                'number_of_comments': submission.num_comments,
                'created_time': datetime.fromtimestamp(submission.created_utc, tz=timezone.utc),
                'post_text': post_text
        })
    return pd.DataFrame(result)


client=Autorization()
result_df=Parse(client,'Proxmox')
print(result_df)
result_df.to_csv('Proxmox_df.csv', index=False)
