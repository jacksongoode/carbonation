import json
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from newsapi import NewsApiClient
from newscatcherapi import NewsCatcherApiClient

load_dotenv()
catcher = NewsCatcherApiClient(x_api_key=os.environ.get("NEWSCATCHER"))
newsapi = NewsApiClient(api_key=os.environ.get("NEWSAPI"))


def download_resource(url, path):
    r = requests.get(url, allow_redirects=True)

    with open(f"resources/{path}.json", "wb") as f:
        f.write(r.content)


def fetch_newscatcher_sources():
    sources = catcher.get_sources(lang="en", countries="US")
    with open("carbonation/resources/sources/newscatcher.json", "w") as f:
        json.dump(sources, f)


def fetch_newsapi_sources():
    sources = newsapi.get_sources(language="en")
    with open("carbonation/resources/sources/newsapi.json", "w") as f:
        json.dump(sources, f)


def fetch_mbfc():
    mbfc = "https://raw.githubusercontent.com/drmikecrowe/mbfcext/main/docs/v4/csources-pretty.json"
    download_resource(mbfc, "bias/mbfc_bias")


def fetch_allsides():
    allsides = "https://www.allsides.com/media-bias/json/noncommercial/all"
    download_resource(allsides, "bias/allsides_bias")


def write_bias():
    # Get urls
    with open("resources/bias/allsides_bias.json", "r") as f:
        allsides = json.load(f)["allsides_media_bias_ratings"]
    as_urls = [s["source_url"] for s in allsides if s["source_url"] != ""]
    as_urls = [".".join(urlparse(url).netloc.split(".")[-2:]) for url in as_urls]

    with open("resources/bias/mbfc_bias.json", "r") as f:
        mbfc = json.load(f)
    mbfc_urls = list(mbfc.keys())
    mbfc_urls = [u for u in mbfc_urls if "/" not in u]

    urls = list(set(as_urls + mbfc_urls))

    with open("carbonation/resources/sources/sources.txt", "w") as f:
        for line in urls:
            f.write(f"{line}\n")
