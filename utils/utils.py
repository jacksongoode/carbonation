import os
import json
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from newsapi import NewsApiClient
from newscatcherapi import NewsCatcherApiClient


load_dotenv()
catcher = NewsCatcherApiClient(x_api_key=os.environ.get('NEWSCATCHER'))
newsapi = NewsApiClient(api_key=os.environ.get('NEWSAPI'))


def get_newscatcher_sources():
    sources = catcher.get_sources(lang='en',
                                        countries='US')

    with open('sources/newscather.json', 'w') as f:
        json.dump(sources, f)


def get_newsapi_sources():
    sources = newsapi.get_sources(language='en')

    with open('sources/newsapi.json', 'w') as f:
        json.dump(sources, f)


def download_bias():
    mbfc = "https://raw.githubusercontent.com/drmikecrowe/mbfcext/main/docs/v4/csources-pretty.json"
    r = requests.get(mbfc, allow_redirects=True)

    with open("sources/mbfc.json", "wb") as f:
        f.write(mbfc)
