import pandas as pd
import twint
from utils import remove_extra_infom
import json

path_celbrity_tweets = "celbrity_tweets.csv"
path_about_celebrity_tweets = "tweets_about_celebrities.csv"
path_celebrity_replies = "celebrity_replies.csv"
celebrities = [
    "Elon Musk"
]
usernames = [
    "elonmusk"

]
words = [" once said", " said", ""]
LIMIT = 15
LANG = "en"


def search_username_tweets(username):
    config = twint.Config()
    config.Search = username
    config.Lang = LANG
    config.Limit = LIMIT
    config.Custom["tweet"] = ["tweet"]
    config.Pandas = True
    config.Hide_output = True
    twint.run.Search(config)
    data_frame = pd.DataFrame(
        twint.storage.panda.Tweets_df["tweet"], columns=[username]
    )
    return remove_extra_infom(data_frame.drop_duplicates(), username)


def search_tweets(username, words):
    TweetsDf = pd.DataFrame(columns=[username])
    for word in words:
        config = twint.Config()
        config.Search = username + word
        config.Lang = LANG
        config.Limit = LIMIT
        config.Custom["tweet"] = ["tweet"]
        config.Pandas = True
        config.Hide_output = True
        twint.run.Search(config)
        TweetsDf = TweetsDf.append(
            pd.DataFrame(
                list(twint.storage.panda.Tweets_df["tweet"]), columns=[username]
            ).drop_duplicates(),
            ignore_index=True,
        )
    result_data_frame = remove_extra_infom(TweetsDf, username)
    result_data_frame.dropna(subset=[username], inplace=True)
    return json.dumps({"pharses":result_data_frame.values.tolist()})


def search_replies(username):
    config = twint.Config()
    config.Search = "-from:{} -filter:replies".format(username)
    config.Lang = LANG
    config.Limit = LIMIT
    config.Custom["tweet"] = ["tweet"]
    config.Pandas = True
    config.Hide_output = False
    twint.run.Search(config)
    data_frame = pd.DataFrame(
        twint.storage.panda.Tweets_df["tweet"], columns=[username]
    )
    return remove_extra_infom(data_frame.drop_duplicates(), username)


if __name__ == "__main__":
    json = search_tweets(celebrities[0],words)
    print(json)
    print(type(json))
    json.loads(json)
    print(json)
    # celebrity_tweets = pd.DataFrame()
    # tweets_about_celebrities = pd.DataFrame()
    # celebrity_replies = pd.DataFrame()
    # for celebrity in usernames:
    #     celebrity_tweets[celebrity] = search_username_tweets(celebrity)
    # for celebrity in celebrities:
    #     tweets_about_celebrities[celebrity] = search_tweets(celebrity, words)
        #celebrity_replies[celebrity] = search_replies(celebrity)
    '''tweets_about_celebrities.to_csv(path_about_celebrity_tweets)
    tweets_about_celebrities.to_csv(path_celbrity_tweets)
    celebrity_replies.to_csv(path_celebrity_replies)'''
