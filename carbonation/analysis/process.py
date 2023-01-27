import json
from datetime import datetime

from carbonation.utils import get_newscatcher_headlines


def fetch_store(hours=1, max_page=10, use_sources=False):
    now = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")

    urls = None
    if use_sources:
        with open("carbonation/resources/sources/sources.txt", "r") as f:
            urls = f.readlines()

    # Get news with urls as sources
    news = get_newscatcher_headlines(hours, sources=urls, max_page=max_page)

    # Write and return news
    with open(f"carbonation/resources/articles/newscatcher_{hours}hr_{now}.json", "w") as f:
        f.write(json.dumps(news))

    return news
