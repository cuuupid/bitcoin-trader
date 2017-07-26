import sys, os
from nltk.corpus import stopwords
import re
word_list = []

f=open('data/train/headlines.csv','r')
sw = set(stopwords.words())
lines=f.readlines()[1:]
i=0
for line in lines:
    new_words = re.sub("[^a-zA-Z]","",line.lower().replace(" ","SPACEBAR")).split("SPACEBAR")
    for word in new_words:
        if word.strip() not in word_list and word.strip() not in sw:
            word_list.append(word.strip())
    i=i+1
    print("[+] Finished line "+str(i)+"/"+str(len(lines)))

f.close()
f=open('data/headlines.wordlist','w')
for word in word_list:
    f.write(word+"\n")
f.close()