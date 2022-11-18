import json
from datetime import datetime

from utils import get_newscatcher_headlines

# from urllib.parse import urlparse



def fetch_store(hours=1):
    now = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")

    # f = open("resources/bias/allsides_bias.json")
    # allsides = json.load(f)["allsides_media_bias_ratings"]
    with open("resources/bias/mbfc_bias.json", "r") as f:
        mbfc = json.load(f)

    # Get urls
    # urls = [s["source_url"] for s in allsides if s["source_url"] != ""]
    # urls = [".".join(urlparse(url).netloc.split(".")[-2:]) for url in urls]
    urls = list(mbfc.keys())
    urls = [u for u in urls if "/" not in u]

    news = get_newscatcher_headlines(hours, max_page=10)

    # Write and return news
    with open(f"resources/articles/newscatcher_{hours}hr_{now}.json", "w") as f:
        f.write(json.dumps(news))

    return news
