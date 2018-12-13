from pymongo import MongoClient


def count_accounts(db):
    '''
        Count used accounts
    '''
    collections = db.collection_names()

    used_accounts = 0
    all_accounts = 0

    for collection in collections:
        tweets = db[collection].find().sort("replies_count", -1)
        all_accounts += 1
        if tweets == 0:
            break
        for tweet in tweets:
            replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
            if replies_count > 0:                             #todo change the number maybe ?????
                used_accounts += 1
                break
    return all_accounts, used_accounts


def count_all(db):
    '''
        counts all the tweets and replies
    '''
    collections = db.collection_names()

    tweets_count = 0
    replies_count = 0

    # Iterate over the data and add the sentiment score to the list
    for collection in collections:
        tweets_count += db[collection].find().count()
        tweets = db[collection].find().sort("replies_count", -1)

        for tweet in tweets:
            replies_count += db[collection].find_one({'id': tweet["id"]})["replies_count"]
    return tweets_count, replies_count



def count_used(db):
    '''
        Counts used tweets and replies, only tweets with more than 20 replies
    '''
    collections = db.collection_names()

    used_tweets_count = 0
    used_replies_count = 0

    # Iterate over the data and add the sentiment score to the list
    for collection in collections:
        tweets = db[collection].find().sort("replies_count", -1)

        for tweet in tweets:
            replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
            if replies_count > 0:
                used_tweets_count += 1
                used_replies_count += replies_count
            # tweets_score.append(tweet["scores"]["sentiment_score"])
    return used_tweets_count, used_replies_count


# connection to Mongo
connection = MongoClient("mongodb://localhost:27017/")

# count accounts
all_real_accounts, used_real_accounts = count_accounts(connection.real_news)
all_fake_accounts, used_fake_accounts = count_accounts(connection.fake_news)

# count all tweets and replies
real_tweets, real_replies = count_all(connection.real_news)
fake_tweets, fake_replies = count_all(connection.fake_news)

# count tweets with more than 20 replies and replies
used_real_tweets, used_real_replies = count_used(connection.real_news)
used_fake_tweets, used_fake_replies = count_used(connection.fake_news)


# write output to file
file = open("output/Counted everything.txt", "w")

file.write("All real accounts: %d\n" % all_real_accounts)
file.write("Used real accounts: %d\n" % used_real_accounts)
file.write("All fake accounts: %d\n" % all_fake_accounts)
file.write("Used fake accounts: %d\n" % used_fake_accounts)
file.write("\n")

file.write("All real tweets: %d\n" % real_tweets)
file.write("All real replies: %d\n" % real_replies)
file.write("All fake tweets: %d\n" % fake_tweets)
file.write("All fake replies: %d\n" % fake_replies)
file.write("\n")

file.write("Used real tweets: %d\n" % used_real_tweets)
file.write("Used real replies: %d\n" % used_real_replies)
file.write("Used fake tweets: %d\n" % used_fake_tweets)
file.write("Used fake replies: %d\n" % used_fake_replies)
file.write("\n")

file.close()
















