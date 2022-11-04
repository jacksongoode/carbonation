import os
import json
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from newsapi import NewsApiClient
from newscatcherapi import NewsCatcherApiClient

load_dotenv()
catcher = NewsCatcherApiClient(x_api_key=os.environ.get('NEWSCATCHER'))
newsapi = NewsApiClient(api_key=os.environ.get('NEWSAPI'))


def hour_window(hours):
    now = datetime.now()
    before = now - timedelta(hours=hours)

    before = before.strftime('%Y-%m-%dT%H:%M:%S')
    now = now.strftime('%Y-%m-%dT%H:%M:%S')

    return before, now


def get_newscatcher_headlines():
    # before, now = hour_window(1)

    articles = catcher.get_latest_headlines_all_pages(
        when='1h',
        lang='en',
        max_page=1,
        seconds_pause=1.0,
    )

    return articles


def get_newsapi(word):
    before, now = hour_window(1)

    articles = newsapi.get_everything(
        q=word,
        from_param=before,
        to=now,
        language='en',
        sort_by='publishedAt'
    )

    return articles


# ! Can't do much... no time filter!
def get_newsapi_headlines():
    headlines = newsapi.get_top_headlines(
        language='en',
        page_size=100)

    return headlines


def split_url(text):
    base = ""
    try:
        groups = text.split('/')
        base = '/'.join(groups[2:3])
    except:
        pass

    return base


app = Flask(__name__)
app.jinja_env.globals.update(split_url=split_url)


@app.route('/page')
def page():
    return render_template('page.html', data=data)


@app.route('/newsapi')
def render_newsapi():
    news = get_newsapi('*')
    data = {
        'articles': news['articles'],
        'total_results': news['totalResults'],
    }

    return render_template('newsapi.html', data=data)


@app.route('/newscatcher')
def render_newscatcher():
    news = get_newscatcher_headlines()
    data = {
        'articles': news['articles'],
        'total_results': news['total_hits'],
    }

    return render_template('newscatcher.html', data=data)
