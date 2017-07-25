import sys, os
from nltk.corpus import stopwords
import re
word_list = []

f=open('data/train/data.csv','r')
sw = stopwords.words()
for line in f.readlines()[1:]:
    new_words = re.sub("[^a-z]","",line.lower()).split()
    for word in new_words:
        if word.strip() not in word_list and word.strip() not in sw:
            word_list.append(word.strip())

f.close()
f=open('data.wordlist','w')
for word in word_list:
    f.write(word+"\n")
f.close()