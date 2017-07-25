from nltk import word_tokenize, NaiveBayesClassifier, FreqDist, classify
from nltk.corpus import stopwords
import re

data = []
f=open('data/train/data.csv','r')
for line in f.readlines()[1:]:
    text, score = line.split('/////')
    data.append([text.strip(),float(score)])

f=open('data/wordlist','r')
all_words = FreqDist(w for w in f.readlines())
word_features=set(all_words)

def create_features(article):
    article_features = set(re.sub("[^a-z]","",article.lower()).split())
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in article_features)
    return features

feature_set = [(create_features(article),score) for (article, score) in data]
training_set, testing_set = feature_set[:int(len(feature_set)*3/4)], feature_set[int(len(feature_set)*3/4):]
print("[*] Training...")
classifier=NaiveBayesClassifier.train(training_set)
print("[+] Finished training.")
print("[=] Accuracy: "+str(classify.accuracy(classifier,testing_set)))
print("")
print("[=] Analyzing features...")
classifier.show_most_informative_features(5)