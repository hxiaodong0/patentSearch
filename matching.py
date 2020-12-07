# https://dev.to/coderasha/compare-documents-similarity-using-python-nlp-4odp

import nltk
import gensim
import numpy as np
nltk.download('punkt')
from nltk.tokenize import word_tokenize , sent_tokenize

#split sentence into words
# data = "Mars is approximately half the diameter of Earth."
# print(word_tokenize(data))
#
# #split paragraph into sentences
# para = "Mars is a cold desert world. It is half the size of Earth. "
# print(sent_tokenize(para))


file_docs = []

with open ('relavo.txt') as f:
    tokens = sent_tokenize(f.read())
    for line in tokens:
        file_docs.append(line)

# print("Number of documents:",len(file_docs))

#Tokenize words and create dictionary

gen_docs = [[w.lower() for w in word_tokenize(text)]
            for text in file_docs]
# print(gen_docs)
dictionary = gensim.corpora.Dictionary(gen_docs)
# print(dictionary.token2id)

# create a bag of words
corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
# print(corpus)

# TFIDF Term Frequency – Inverse Document Frequency(TF-IDF)

# words that occur more frequently across the documents get smaller weights.
tf_idf = gensim.models.TfidfModel(corpus)
lst = []
for doc in tf_idf[corpus]:
    lst.append([[dictionary[id], np.around(freq, decimals=2)] for id, freq in doc])
    print([[dictionary[id], np.around(freq, decimals=2)] for id, freq in doc])


dic = {}
for item in lst:
    for i in item:
        if i[0] not in dic.keys():
            dic[i[0]] = i[1]
