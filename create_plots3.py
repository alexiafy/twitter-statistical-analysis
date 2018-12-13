from pymongo import MongoClient
import re
import matplotlib.pyplot as plt
import numpy as np

connection = MongoClient("mongodb://localhost:27017/")
db = connection.fake_news                     # name of db (it should be changed to real_news or fake_news
collections = db.collection_names()



# get controversial words from bias lexicon
file1 = open('input/bias-lexicon.txt', 'r')
text = file1.read()

words = text.split("\n")

bias_counter = 0
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
                bias_word_exists = False
                reply_text = reply["text"].lower()

                all_replies += 1

                # check if at least one controversy word is included
                for word in words:
                    if re.search(r"\b" + re.escape(word) + r"\b", reply_text):
                        bias_word_exists = True
                if bias_word_exists:
                    bias_counter += 1

file1.close()
print("All replies: ", all_replies)
print("Bias word replies: ", bias_counter)






# get controversial words from Mejova controversy lexicon
file2 = open('input/controversial_words.txt', 'r')
text = file2.read()

words = text.split(", ")

contr_counter = 0

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

                # check if at least one controversy word is included
                for word in words:
                    if re.search(r"\b" + re.escape(word) + r"\b", reply_text):
                        contr_word_exists = True
                if contr_word_exists:
                    contr_counter += 1

file2.close()
print("All replies: ", all_replies)
print("Controversy word replies: ", contr_counter)





# get skepticism words from skepticism lexicon
file3 = open('input/skepticism_words.txt', 'r')
text = file3.read()

words = text.split(", ")

skepticism_counter = 0

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
                skepticism_word_exists = False
                reply_text = reply["text"].lower()

                # check if at least one controversy word is included
                for word in words:
                    if re.search(r"\b" + re.escape(word) + r"\b", reply_text):
                        skepticism_word_exists = True
                if skepticism_word_exists:
                    skepticism_counter += 1

file3.close()
print("All replies: ", all_replies)
print("Controversy word replies: ", skepticism_counter)




# write results to file
file4 = open('input/Fake news - words_results.txt', 'w')
file4.write("%d replies with bias words out of %d replies \n" % (bias_counter,all_replies))
file4.write("%d replies with controversy words out of %d replies \n" % (contr_counter,all_replies))
file4.write("%d replies with skepticism words out of %d replies \n" % (skepticism_counter,all_replies))
file4.close()


# create plot
n_groups = 3
controversy_replies = (bias_counter, contr_counter, skepticism_counter)
no_controversy_replies = (all_replies - bias_counter, all_replies - contr_counter, all_replies - skepticism_counter)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.25
opacity = 0.8

rects1 = plt.bar(index, controversy_replies, bar_width,
                 alpha=opacity,
                 color=(0.2, 0.4, 0.6, 0.9),
                 label='With',
                 zorder=3)

rects2 = plt.bar(index + bar_width, no_controversy_replies, bar_width,
                 alpha=opacity,
                 color=(0.6, 0.3, 0.5, 0.9),
                 label='Without',
                 zorder=3)

plt.legend(loc=4)
plt.ylabel('Number of replies')
plt.title('Fake news - percentage of replies with and without controversial words')
plt.xticks(index + bar_width/2, ('Bias lexicon', 'Controversy lexicon', 'Skepticism lexicon'),
           rotation=45, ha="right")


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 0.99*height,
                '%d %%' % int(height*100/all_replies),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

ax.yaxis.grid(linestyle=':', zorder=0)
plt.tight_layout()

plt.savefig("plots/Fake news - Replies with controversy words.svg")
plt.show()



