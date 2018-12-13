from pymongo import MongoClient


connection1 = MongoClient("mongodb://localhost:27017/")
db1 = connection1.real_news                     # name of db (it should be changed to real_news or fake_news
collections1 = db1.collection_names()


contr_counter1 = 0
all_replies1 = 0
# Iterate over the data and write it out row by row.
for collection in collections1:
    tweets = db1[collection].find().sort("replies_count", -1).batch_size(10)
    for tweet in tweets:
        replies_count = db1[collection].find_one({'id': tweet["id"]})["replies_count"]
        if replies_count > 200:
            all_replies1 += 1
            if(tweet["scores"]["sentiment_score"]) > 0.5:
                contr_counter1 += 1

print("Real - Ποσοστό των replies με controversy score μεγαλύτερο από 0.7", contr_counter1/all_replies1*100)


connection2 = MongoClient("mongodb://localhost:27017/")
db2 = connection2.fake_news
collections2 = db2.collection_names()

contr_counter2 = 0
all_replies2 = 0
# Iterate over the data and write it out row by row.
for collection in collections2:
    tweets = db2[collection].find().sort("replies_count", -1).batch_size(10)
    for tweet in tweets:
        replies_count = db2[collection].find_one({'id': tweet["id"]})["replies_count"]
        if replies_count > 200:
            all_replies2 += 1
            if(tweet["scores"]["sentiment_score"]) > 0.5:
                contr_counter2 += 1

print("Fake - Ποσοστό των replies με controversy score μεγαλύτερο από 0.7", contr_counter2/all_replies2*100)


