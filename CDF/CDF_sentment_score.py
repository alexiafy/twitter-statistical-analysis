from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np

# compute ecdf
def ecdf(data):
    xaxis = np.sort(data)              #sort the data
    yaxis = np.arange(1, len(data)+1)/len(data)    #create percentages for y axis from 1% to 100%
    return xaxis, yaxis


# take data from database
def take_data(db):
    collections = db.collection_names()

    tweets_score = []

    # Iterate over the data and add the sentiment score to the list
    for collection in collections:
        tweets = db[collection].find().sort("replies_count", -1).batch_size(10)
        for tweet in tweets:
            replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
            if replies_count > 150:
                tweets_score.append(tweet["ratios"]["pnpnt"])
    return tweets_score


# connection to Mongo
connection = MongoClient("mongodb://localhost:27017/")
real_data = take_data(connection.real_news)
fake_data = take_data(connection.fake_news)

# ecdf
x_real, y_real = ecdf(real_data)
x_fake, y_fake = ecdf(fake_data)

plt.plot(y_real, x_real, marker='.', linestyle='-', color='blue', label='real news')
plt.plot(y_fake, x_fake, marker='.', linestyle='-', color='red', label='fake news')

plt.title('ECDF Plot of pnpnt ratio')
plt.xlabel('Percent of tweets')
plt.ylabel('Pnpnt ratio')
plt.yticks(np.arange(0, 1.1, 0.1))
plt.grid(linestyle=':')
legend = plt.legend(loc=6, bbox_to_anchor=(1, 0.5))


plt.savefig("../plots/CDF plots/Pnpnt ratio.svg", bbox_extra_artists=(legend,), bbox_inches='tight')
plt.show()


