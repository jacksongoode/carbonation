import json
from urllib.parse import urlparse
from datetime import datetime

from utils import get_newscatcher_headlines, download_resource


def fetch_store():
    hours = 4
    now = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")

    f = open('resources/bias/allsides_bias.json')
    allsides = json.load(f)["allsides_media_bias_ratings"]

    # Get urls
    urls = [s['source_url'] for s in allsides if s['source_url'] != '']
    urls = ['.'.join(urlparse(url).netloc.split('.')[-2:]) for url in urls]
    res = get_newscatcher_headlines(hours, sources=urls, max_page=10)

    with open(f"articles/newscatcher_{hours}_{now}.json", "w") as f:
        f.write(json.dumps(res))

    return res

    # headlines = get_newscatcher_headlines(4)
