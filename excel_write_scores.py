from pymongo import MongoClient
import xlsxwriter



connection = MongoClient("mongodb://localhost:27017/")
db = connection.real_news                     # name of db (it should be changed to real_news or fake_news
collections = db.collection_names()


# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('output/SCORES - controversy results real.xlsx')
worksheet = workbook.add_worksheet()

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': 1})

# set column width
worksheet.set_column(0, 2, 23)
worksheet.set_column(3, 9, 15)



# Write some data headers.
worksheet.write('A1', 'Account name', bold)
worksheet.write('B1', 'Account ID', bold)
worksheet.write('C1', 'Tweet ID', bold)
worksheet.write('D1', 'Replies count', bold)
worksheet.write('E1', 'Positive replies', bold)
worksheet.write('F1', 'Negative replies', bold)
worksheet.write('G1', 'Neutral replies', bold)
worksheet.write('H1', 'Sentiment score', bold)
worksheet.write('I1', 'Language score', bold)
worksheet.write('J1', 'Intensity score', bold)

# Start from the first cell. Rows and columns are zero indexed.
row = 1
col = 0

# Iterate over the data and write it out row by row.
for collection in collections:
    tweets = db[collection].find().sort("replies_count", -1).batch_size(10)
    for tweet in tweets:
        replies_count = db[collection].find_one({'id': tweet["id"]})["replies_count"]
        if replies_count > 0:
            print(tweet["id"])
            worksheet.write(row, col, tweet["user"]["screen_name"])
            worksheet.write(row, col + 1, collection)
            worksheet.write(row, col + 2, str(tweet["id"]))
            worksheet.write_number(row, col + 3, tweet["replies_count"])
            worksheet.write_number(row, col + 4, tweet["replies_sentiment"]["positive_replies"])
            worksheet.write_number(row, col + 5, tweet["replies_sentiment"]["negative_replies"])
            worksheet.write_number(row, col + 6, tweet["replies_sentiment"]["neutral_replies"])
            worksheet.write_number(row, col + 7, tweet["scores"]["sentiment_score"])
            worksheet.write_number(row, col + 8, tweet["scores"]["language_score"])
            worksheet.write_number(row, col + 9, tweet["scores"]["intensity_score"])
            row += 1


workbook.close()



