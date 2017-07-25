from nltk import word_tokenize, NaiveBayesClassifier, FreqDist, classify
from nltk.corpus import stopwords
import re
import pickle

print("[=] Reading headlines...")
data = []
f=open('data/train/headlines.csv','r')
for line in f.readlines()[1:]:
    if len(line)>10 and ',' in line:
        try:
            text, score = line.split(',')
            data.append([text.strip(),float(score)])
        except:
            pass
f.close()
print("[+] Read headlines.")
f=open('data/headlines.wordlist','r')
print("[=] Generating wordlist...")
all_words = FreqDist(w for w in f.readlines())
word_features=set(all_words)
print("[+] Generated wordlist.")
f.close()
def create_features(article):
    article_features = set(re.sub("[^a-z]","",article.lower()).split())
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in article_features)
    return features

print("[=] Generating features...")
feature_set = []
i=0
for (article, score) in data[:500]:
    feature_set.append([create_features(article),score])
    i=i+1
    print("Generated feature "+str(i)+"/"+str(len(data)))
print("[+] Generated features...")
training_set, testing_set = feature_set[:int(len(feature_set)*3/4)], feature_set[int(len(feature_set)*3/4):]
print("[+] Generated training set of length "+str(len(training_set))+", and testing set of length "+str(len(testing_set)))
print("[*] Training...")
classifier=NaiveBayesClassifier.train(training_set)
print("[+] Finished training.")
f_dos=open('models/checkpoints/headline_classifier.pickle','wb')
pickle.dump(classifier,f_dos)
f_dos.close()
print("[+] Saved classifier.")
print("[=] Accuracy: "+str(classify.accuracy(classifier,testing_set)))
print("")
print("[=] Analyzing features...")
classifier.show_most_informative_features(5)