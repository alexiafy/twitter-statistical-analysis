# get controversial words from txt file
file = open('input/dispute_words.txt', 'r')
text = file.read()
print(text)
words = text.split(", ")

words.sort()
print(words)

file2 = open('input/dispute_words2.txt', 'w')
for word in words:
    file2.write(word + ", ")

file.close()
file2.close()