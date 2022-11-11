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


@app.route('/about')
def about():
    return render_template('about.html')


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
    news = get_newscatcher_headlines(1)
    data = {
        'articles': news.get('articles', ''),
        'total_results': news['total_hits']
    }

    return render_template('newscatcher.html', data=data)


@app.route('/model')
def render_model():
    model_fn = 'bert_4hr_11-05-2022_11:33:12.json'
    news = json.load(open(f'resources/computed/{model_fn}'))

    return render_template('model.html', data=news)


if __name__ == '__main__':
    app.run()
