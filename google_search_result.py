from bs4 import BeautifulSoup
import requests
import pandas as pd
from textblob import TextBlob
from flask import Flask, jsonify, request
from urllib.request import urlopen as uReq

app = Flask(__name__)


class Analysis:
    def __init__(self, term):
        self.term = term
        self.sentiment = 0
        self.subjectivity = 0
        self.url = 'https://www.google.com/search?q={0}&source=lnms&tbm=nws'.format(self.term)

    def run(self):
        response = requests.get(self.url)
        print(response)
        # soup = BeautifulSoup(response.text, 'html.parser')
        # headline_results = soup.find_all('div', class_='st')
        # for text in headline_results:
        #     blob = TextBlob(text.get_text())
        #     self.sentiment += blob.sentiment.polarity / len(headline_results)
        #     self.subjectivity += blob.sentiment.subjectivity / len(headline_results)
url1 = 'https://relavomedical.com/'
url = 'https://www.google.com/search?q={0}&source=lnms&tbm=nws'.format('bitcoin')

uClient = uReq(url1)
page_html = uClient.read()
response = requests.get(url)





# a = Analysis('bitcoin')
# a.run()

# @app.route('/analyze')
# def sentiment():
#     if request.method == 'GET':
#         term = request.args.get('term')
#         analysis = Analysis.Analysis(term)
#         analysis.run()
#         return jsonify({"Term": term, "Sentiment": analysis.sentiment, "Subjectivity": analysis.subjectivity})
#     else:
#         return ('USE GET REQUEST PLZ')
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
