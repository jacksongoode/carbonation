import json
from datetime import datetime
# from urllib.parse import urlparse

from utils import get_newscatcher_headlines


def fetch_store(hours=1):
    now = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")

    # Get urls
    # with open("resources/bias/allsides_bias.json", "r") as f:
    #     allsides = json.load(f)["allsides_media_bias_ratings"]
    # as_urls = [s["source_url"] for s in allsides if s["source_url"] != ""]
    # as_urls = [".".join(urlparse(url).netloc.split(".")[-2:]) for url in as_urls]

    # with open("resources/bias/mbfc_bias.json", "r") as f:
    #     mbfc = json.load(f)
    # mbfc_urls = list(mbfc.keys())
    # mbfc_urls = [u for u in mbfc_urls if "/" not in u]

    # urls = list(set(as_urls + mbfc_urls))

    # Get news with urls as sources
    news = get_newscatcher_headlines(hours, max_page=25)

    # Write and return news
    with open(f"resources/articles/newscatcher_{hours}hr_{now}.json", "w") as f:
        f.write(json.dumps(news))

    return news
