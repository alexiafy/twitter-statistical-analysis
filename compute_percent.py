from pymongo import MongoClient


connection = MongoClient("mongodb://localhost:27017/")
db = connection.real_news                     # name of db (it should be changed to real_news or fake_news
collections = db.collection_names()


for collection in collections:
    count_sentiment = 0
    counter = 0
    tweets = db[collection].find().sort("replies_count", -1).batch_size(10)
    for tweet in tweets:
        replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
        if replies_count > 20:
            counter +=1
            if tweet["sentiment_score"]>0.5:
                count_sentiment += 1

    if counter:
        percentage = count_sentiment/counter
        print(percentage)
        print(count_sentiment, "στα ", counter)
