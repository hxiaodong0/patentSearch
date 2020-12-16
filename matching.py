#Running time approximately: <1hour
#reference sites https://dev.to/coderasha/compare-documents-similarity-using-python-nlp-4odp
import string
import nltk
import gensim
import numpy as np
nltk.download('punkt')
from nltk.tokenize import word_tokenize , sent_tokenize
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm
import time

def compare_weights(weights_relavo, weights):
    """
    This function returns the weights relative to the Relavo patent

    :rtype: dictionary
    """
    n = 0
    for key,val in weights.items():
        if key in weights_relavo:
            n += round(val * weights_relavo[key], 2)
    return n

def get_weights(filename = 'relavo.txt', txt_or_lst = "txt"): # txt is inputing a txt file, str is inputing a list[string] file.
    """
    This function computes the weights of the key words, the weights is computed by weighted occurrences.
    # TFIDF Term Frequency – Inverse Document Frequency(TF-IDF)

    :rtype: dictionary
    """
    file_docs = []
    if txt_or_lst == 'txt':
        with open (str(filename)) as f:
            tokens = sent_tokenize(f.read())
            for line in tokens:
                file_docs.append(line)
    else:
        file_docs = filename
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
    # words that occur more frequently across the documents get bigger weights.
    tf_idf = gensim.models.TfidfModel(corpus)
    lst = []
    for doc in tf_idf[corpus]:
        lst.append([[dictionary[id], np.around(freq, decimals=2)] for id, freq in doc])
        # print([[dictionary[id], np.around(freq, decimals=2)] for id, freq in doc])


    #  This section is to remove all the words that are not relavent : integers, punctuation, for, from, to, the, etc.
    prep = ("when","or","further","is","claim","wherein","that","keep","causes","a","and","are","be","an","aboard","about","above","across","after","against","along","amid","among","anti","around","as","at","before","behind","below","beneath","beside","besides","between","beyond","but","by","concerning","considering"
    ,"despite","down","during","except","excepting","excluding","following","for","from","in","inside","into","like","minus","near","of","off","on","onto","opposite","outside","over","past","per","plus","regarding","round","save","since"
    ,"than","through","to","toward","towards","under","underneath","unlike","until","up","upon","versus","via","with","within","without")
    dic = {}
    for item in lst:
        for i in item:
            if i[0] not in dic.keys():
                dic[i[0]] = i[1]
            else:
                dic[i[0]] = round(dic[i[0]] + i[1], 2)

    dic_copy = dic.copy()
    for key, val in dic_copy.items():
        if key in string.punctuation or key in prep:
            dic.pop(key)
        try:
          (int(key))
          dic.pop(key)
        except:
          continue

    return dic

def main(USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"):
    """

    :rtype: object
    """
    results = {}
    file = pd.ExcelFile('Relavo_patent_search_keywords.xlsx')
    print("Loading file successful, the sheets names are: ", file.sheet_names) # to view the sheets name
    df = file.parse("All_search_results") # make a dataframe from the "All_search results sheet"  "retraction; syringe"
    res = df["result link"]#'result link'
    len = res.__len__()
    weights_relavo = get_weights()
    df.insert(12, "KeyWord Similarity score", "N\A")
    print("being process")
    for i in tqdm(range(len)):

        URL = res[i]

        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"


        headers = {"user-agent": USER_AGENT}
        try:
            resp = requests.get(URL, headers=headers)
        except:
            print("request failed",URL)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            claim_txt = []
            for g in soup.find_all('div', class_='claim-text'):
                claim_txt.append(g.get_text())
            weights = get_weights(claim_txt, "lst")
            n = compare_weights(weights_relavo, weights)
            df.at[i, "KeyWord Similarity score"] = n
        else:
            continue

    print("process complete, total time is: ",time.time() - start_time ,"Total number of search terms are: ",len )
    return df
if __name__ == '__main__':
    start_time = time.time()
    # desktop user-agent
    # ###################################
    # IMPORTANT                              go to chrome, search my user agent, copy the User agent into the User_agent down below.
    # ###################################
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    df = main(USER_AGENT) # call the main function.
    df.to_excel("Search_results with relevance weights.xlsx") # export the datefram to excel

