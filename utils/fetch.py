
import os
import json

import requests
from dotenv import load_dotenv
from newsapi import NewsApiClient
from newscatcherapi import NewsCatcherApiClient

load_dotenv()
catcher = NewsCatcherApiClient(x_api_key=os.environ.get('NEWSCATCHER'))
newsapi = NewsApiClient(api_key=os.environ.get('NEWSAPI'))


def download_resource(url, path):
    r = requests.get(url, allow_redirects=True)

    with open(f"resources/{path}.json", "wb") as f:
        f.write(r.content)


def fetch_newscatcher_sources():
    sources = catcher.get_sources(lang='en', countries='US')
    with open('resources/sources/newscatcher.json', 'w') as f:
        json.dump(sources, f)


def fetch_newsapi_sources():
    sources = newsapi.get_sources(language='en')
    with open('resources/sources/newsapi.json', 'w') as f:
        json.dump(sources, f)


def fetch_mbfc():
    mbfc = "https://raw.githubusercontent.com/drmikecrowe/mbfcext/main/docs/v4/csources-pretty.json"
    download_resource(mbfc, "bias/mbfc_bias")


def fetch_allsides():
    allsides = "https://www.allsides.com/media-bias/json/noncommercial/all"
    download_resource(allsides, "bias/allsides_bias")
