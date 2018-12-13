from pymongo import MongoClient
import matplotlib.pyplot as plt

connection = MongoClient("mongodb://localhost:27017/")
db = connection.real_news                     # name of db (it should be changed to real_news or fake_news
collections = db.collection_names()


percentage_dict = dict()


'''for collection in collections:
    sentiment_counter = 0
    tweets = db[collection].find().sort("replies_count", -1).batch_size(10)
    for tweet in tweets:
        replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
        if replies_count > 0:
            if tweet["sentiment_score"] > 0.5:
                sentiment_counter += 1

            account_name = tweet["user"]["screen_name"]

    if tweets.count() != 0:
        percentage_dict[account_name] = sentiment_counter/tweets.count()*100
    else:
        account_name = collection
        percentage_dict[account_name] = 0

print(percentage_dict)


plt.bar(range(len(percentage_dict)), list(percentage_dict.values()), align='center', color=(0.2, 0.4, 0.6, 0.7))
plt.xticks(range(len(percentage_dict)), list(percentage_dict.keys()))
plt.xticks(rotation=45, ha="right")

plt.title('Ποσοστό των tweets με sentiment_score > 0,5 (μη "έμπιστοι" λογαριασμοί)')
plt.xlabel('Όνομα λογαριασμού')
plt.ylabel('Ποσοστό (%)')
plt.grid(linestyle=':')
plt.tight_layout()

plt.savefig("plots/percentage_fake.svg")
plt.show()'''






'''for collection in collections:
    sentiment_counter = 0
    tweets = db[collection].find().sort("replies_count", -1).batch_size(10)
    for tweet in tweets:
        replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
        if replies_count > 0:
            sentiment_counter += abs(tweet["sentiment_score"])
        account_name = tweet["user"]["screen_name"]
        percentage_dict[account_name] = sentiment_counter/tweets.count()

    if tweets.count() == 0:
        account_name = collection
        percentage_dict[account_name] = 0

print(percentage_dict)


plt.bar(range(len(percentage_dict)), list(percentage_dict.values()), align='center', color=(0.2, 0.4, 0.6, 0.7))
plt.xticks(range(len(percentage_dict)), list(percentage_dict.keys()))
plt.xticks(rotation=45, ha="right")

plt.title('Αριθμός των tweets που συλλέχθηκαν από μη έμπιστους λογαριασμούς')
plt.xlabel('Όνομα λογαριασμού')
plt.ylabel('Tweets')
plt.grid(linestyle=':')
plt.tight_layout()

plt.savefig("plots/fake.svg")
plt.show()'''






positive_replies = 0
negative_replies = 0
neutral_replies = 0

for collection in collections:
    tweets = db[collection].find().sort("replies_count", -1).batch_size(10)
    for tweet in tweets:
        replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
        if replies_count > 0:
            positive_replies += tweet["positive_replies"]
            negative_replies += tweet["negative_replies"]
            neutral_replies += tweet["neutral_replies"]


# create plot
labels = 'Positive', 'Negative', 'Neutral'
sizes = [positive_replies, negative_replies, neutral_replies]
colors = [(0.2, 0.4, 0.6, 0.9), (0.2, 0.6, 0.6, 0.8), (0.6, 0.3, 0.5, 0.9)]

fig1, ax1 = plt.subplots()
wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

ax1.legend(wedges, labels, title="Sentiment", loc="center left", bbox_to_anchor=(0.8, 1))
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.savefig("plots/real_sentiment.svg")

plt.show()
