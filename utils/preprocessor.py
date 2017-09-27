import re

def tokenize(words):
    return re.sub("[^a-z ]",'',words.lower()).replace("  "," ").split(" ") #no punctuation all lowercase list of words

def count_vectorizer(word_list):
    dictionary = dict()
    for word in word_list:
        dictionary[word] = 1 if word not in dictionary else dictionary[word]+1
    return dictionary

def one_hot_vectorizer(word_list):
    words = list(set(word_list))
    if '' in words:
        words.remove('')
    one_hot_encoding = list(range(len(words)))
    return dict(zip(words,one_hot_encoding)), dict(zip(one_hot_encoding,words))