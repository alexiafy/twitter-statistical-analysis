from pymongo import MongoClient
import matplotlib.pyplot as plt


connection1 = MongoClient("mongodb://localhost:27017/")
db1 = connection1.real_news                     # name of db (it should be changed to real_news or fake_news
collections1 = db1.collection_names()

real_dict = dict()

contr_counter1 = 0
all_replies1 = 0
# Iterate over the data and write it out row by row.
for collection in collections1:
    tweets = db1[collection].find().sort("replies_count", -1).batch_size(10)
    for tweet in tweets:
        replies_count = db1[collection].find_one({'id': tweet["id"]})["replies_count"]
        if replies_count > 150:
            #if tweet["ratios"]["pnpnt"] > 1.0:
                #continue
            all_replies1 += 1
            if(tweet["ratios"]["pnpnt"]) > 0.3:
                contr_counter1 += 1
            real_dict[tweet["id"]] = tweet["ratios"]["pnpnt"]


print("Real - Ποσοστό των replies με ratio μεγαλύτερο από 0.7", contr_counter1/all_replies1*100)
print(contr_counter1)
print(real_dict)


connection2 = MongoClient("mongodb://localhost:27017/")
db2 = connection2.fake_news
collections2 = db2.collection_names()

fake_dict = dict()


contr_counter2 = 0
all_replies2 = 0
# Iterate over the data and write it out row by row.
for collection in collections2:
    tweets = db2[collection].find().sort("replies_count", -1).batch_size(10)
    for tweet in tweets:
        replies_count = db2[collection].find_one({'id': tweet["id"]})["replies_count"]
        if replies_count > 150:
            #if tweet["ratios"]["pnpnt"] > 1.0:
                #continue
            all_replies2 += 1
            if(tweet["ratios"]["pnpnt"]) > 0.3:
                contr_counter2 += 1
            fake_dict[tweet["id"]] = tweet["ratios"]["pnpnt"]

print("Fake - Ποσοστό των replies με ratio μεγαλύτερο από 0.7", contr_counter2/all_replies2*100)
print(contr_counter2)
fake_dict = {k: fake_dict[k] for k in list(fake_dict)[:len(real_dict)]}
print(fake_dict)

# real news plot
plt.bar(range(len(real_dict)), list(real_dict.values()), align='center', color=(0.2, 0.4, 0.6, 0.7))
plt.xticks(range(len(real_dict)), list(real_dict.keys()))
plt.xticks(rotation=45, ha="right")

plt.title('Real news - PNPNT ratio (tweets with more than 150 replies)')
plt.xlabel('Tweet id')
plt.ylabel('RPN ratio')
plt.grid(linestyle=':')
plt.tight_layout()

plt.savefig("plots/Real news - PNPNT ratio.svg")
plt.show()



# fake news plot
plt.bar(range(len(fake_dict)), list(fake_dict.values()), align='center', color=(0.2, 0.4, 0.6, 0.7))
plt.xticks(range(len(fake_dict)), list(fake_dict.keys()))
plt.xticks(rotation=45, ha="right")

plt.title('Fake news - PNPNT ratio (tweets with more than 150 replies)')
plt.xlabel('Tweet id')
plt.ylabel('RPN ratio')
plt.grid(linestyle=':')
plt.tight_layout()

plt.savefig("plots/Fake news - PNPNT ratio.svg")
plt.show()
