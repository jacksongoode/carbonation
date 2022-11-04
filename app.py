import json
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from newsapi import NewsApiClient
from newscatcherapi import NewsCatcherApiClient

from utils import get_newsapi, get_newscatcher_headlines, split_url
from analysis import job1

load_dotenv()
catcher = NewsCatcherApiClient(x_api_key=os.environ.get('NEWSCATCHER'))
newsapi = NewsApiClient(api_key=os.environ.get('NEWSAPI'))

# set configuration values


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.jinja_env.globals.update(split_url=split_url)
app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)


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


if __name__ == '__main__':
    app.run()
