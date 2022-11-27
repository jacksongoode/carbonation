import json
from datetime import datetime

from utils import get_newscatcher_headlines

# from urllib.parse import urlparse


def fetch_store(hours=1):
    now = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")

    with open("resources/sources/sources.txt", "r") as f:
        urls = f.readlines()

    # Get news with urls as sources
    news = get_newscatcher_headlines(hours, sources=urls, max_page=1)

    # Write and return news
    with open(f"resources/articles/newscatcher_{hours}hr_{now}.json", "w") as f:
        f.write(json.dumps(news))

    return news
