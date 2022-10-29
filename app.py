import json

from flask import Flask, render_template
from flask_apscheduler import APScheduler
from newsapi import NewsApiClient
from newscatcherapi import NewsCatcherApiClient
from random_word import Wordnik

newscatcherapi = NewsCatcherApiClient(
    x_api_key='b_Gopvrwzl8fDrtDn-z__6jY1eAvUJ-Zk8lhstwb1UM')

# Init
newsapi = NewsApiClient(api_key='5a3f0af6add84d15997ea15da457f2bf')

wn = Wordnik()


def get_newscatcher():
    articles = newscatcherapi.get_search(q="Trump", lang='en',
                                         page_size=20)
    return articles


def get_newsapi(word):
    articles = newsapi.get_everything(q=word, language='en')
    return articles


app = Flask(__name__)


@app.route("/")
def data():
    word = wn.get_random_word()
    data = {
        "word": word,
        "articles": get_newsapi(word)
    }
    print(data)
    return render_template('data.html', data=data)
