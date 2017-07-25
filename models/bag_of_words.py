import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from nltk.corpus import stopwords
train=#dataset
test=#dataset
train_reviews=#array of reviews
train_sentiment=#array of sentiment

def sanitize(inp):
    inp=re.sub("[^a-z]"," ",inp.lower()).split()
    stops=set()

vectorizer = CountVectorizer(analyzer='word',tokenizer=None,preprocessor=None,stop_words=None,max_features=5000)
train_data_features=vectorizer.fit_transform(train_reviews)
np.asarray(train_data_features)
forest=RandomForestClassifier(n_estimators=100)
forest=forest.fit(train_data_features, train_sentiment)
#forest.predict(new_data_features)