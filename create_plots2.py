from pymongo import MongoClient
import re
import matplotlib.pyplot as plt

connection = MongoClient("mongodb://localhost:27017/")
db = connection.real_news                     # name of db (it should be changed to real_news or fake_news
collections = db.collection_names()

# get controversial words from txt file
file = open('input/controversial_words.txt', 'r')
text = file.read()

words = text.split(" ")

contr_counter = 0
all_replies = 0

for collection in collections:
    if collection == "25073877":
        print("Skip realDonaldTrump")
        continue
    tweets = db[collection].find().sort("replies_count", -1).batch_size(10)
    for tweet in tweets:
        replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
        if replies_count > 20:
            replies = db[collection].find_one({'id': tweet["id"]})["replies"]
            # count replies with at least one controversy word
            for reply in replies:
                contr_word_exists = False
                reply_text = reply["text"].lower()

                all_replies += 1

                # check if at least one controversy word is included
                for word in words:
                    #if word in reply_text:
                    if re.search(r"\b" + re.escape(word) + r"\b", reply_text):
                        #print(reply_text)
                        #print(word)
                        contr_word_exists = True
                if contr_word_exists:
                    contr_counter += 1

print("All replies: ", all_replies)
print("Controversy word replies: ", contr_counter)
file.close()


labels = 'Replies with controversy words', 'Replies without controversy words'
sizes = [contr_counter, all_replies-contr_counter]
colors = [(0.2, 0.4, 0.6, 0.9), (0.2, 0.6, 0.6, 0.8)]

fig1, ax1 = plt.subplots()
wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

ax1.legend(wedges, labels, loc="center left", bbox_to_anchor=(0.8, 1))
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title("Fake news - Percentage of replies with controversy words from Mejova controversy lexicon")
plt.savefig("plots/Fake news - Controversy_lexicon.svg")

plt.show()

'''all_words = 0
contr_counter = 0
words_counter = 0
all_replies = 0

for collection in collections:
    tweets = db[collection].find().sort("replies_count", -1).batch_size(10)
    for tweet in tweets:
        replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
        if replies_count > 20:
            replies = db[collection].find_one({'id': tweet["id"]})["replies"]
            # count replies with at least one controversy word
            for reply in replies:
                all_replies += 1

                contr_word_exists = False
                reply_text = reply["text"].lower()

                all_words += len(reply_text.split())

                # check if at least one controversy word is included
                for word in words:
                    if word in reply_text:
                        words_counter += 1
                        contr_word_exists = True
                if contr_word_exists:
                    contr_counter += 1

print("All replies: ", all_replies)
print("Controversy word replies: ", contr_counter)
print("All words: ", all_words)
print("Controversy words: ", words_counter)
'''













'''positive_tweets = 0
negative_tweets = 0

for collection in collections:
    tweets = db[collection].find().sort("replies_count", -1).batch_size(10)
    for tweet in tweets:
        replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
        if replies_count > 50:
            if tweet["positive_replies"] > tweet["negative_replies"]:
                positive_tweets += 1
            else:
                negative_tweets += 1

print("Positive tweets: ", positive_tweets)
print("Negative tweets: ", negative_tweets)'''




# create plot
'''labels = 'Positive', 'Negative', 'Neutral'
sizes = [positive_replies, negative_replies, neutral_replies]
colors = [(0.2, 0.4, 0.6, 0.9), (0.2, 0.6, 0.6, 0.8), (0.6, 0.3, 0.5, 0.9)]

fig1, ax1 = plt.subplots()
wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

ax1.legend(wedges, labels, title="Sentiment", loc="center left", bbox_to_anchor=(0.8, 1))
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.savefig("plots/real_sentiment.svg")

plt.show()'''