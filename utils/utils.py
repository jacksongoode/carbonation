import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
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


def get_newscatcher_headlines(hours, sources=None, max_page=1):
    # before, now = hour_window(1)

    articles = catcher.get_latest_headlines_all_pages(
        when=f'{hours}h',
        lang='en',
        sources=sources,
        max_page=max_page,
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
