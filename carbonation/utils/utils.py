import glob
import json
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from newsapi import NewsApiClient
from newscatcherapi import NewsCatcherApiClient

load_dotenv()
catcher = NewsCatcherApiClient(x_api_key=os.environ.get("NEWSCATCHER"))
newsapi = NewsApiClient(api_key=os.environ.get("NEWSAPI"))


def hour_window(hours):
    now = datetime.now()
    before = now - timedelta(hours=hours)

    before = before.strftime("%Y-%m-%dT%H:%M:%S")
    now = now.strftime("%Y-%m-%dT%H:%M:%S")

    return before, now


def get_newscatcher_headlines(hours, sources=None, max_page=1):
    before, now = hour_window(hours)

    with open("carbonation/resources/sources/bad_sources.txt", "r") as f:
        bad_sources = f.readlines()

    # articles = catcher.get_latest_headlines_all_pages(
    #     when=f"{hours}h",
    #     lang="en",
    #     sources=sources,
    #     max_page=max_page,
    #     seconds_pause=1.0,
    #     to_rank=1000,
    #     sort_by="rank"
    # )

    articles = catcher.get_search_all_pages(
        # when=f"{hours}h",
        q="*",
        from_=before,
        to_=now,
        lang="en",
        not_sources=bad_sources,
        sources=sources,
        max_page=max_page,
        seconds_pause=1.0,
        to_rank=500,
        # sort_by="date",
    )

    return articles


def get_newsapi(word):
    before, now = hour_window(1)

    articles = newsapi.get_everything(
        q=word, from_param=before, to=now, language="en", sort_by="publishedAt"
    )

    return articles


# ! Can't do much... no time filter!
def get_newsapi_headlines():
    headlines = newsapi.get_top_headlines(language="en", page_size=100)

    return headlines


def split_url(text):
    base = ""
    try:
        groups = text.split("/")
        base = "/".join(groups[2:3])
    except Exception():
        pass

    return base


def merge(source, destination):
    """Destination overrides source."""
    for key, value in source.items():
        if isinstance(value, dict):
            merge(value, destination.setdefault(key, {}))
        elif key in ["rights", "twitter_account"]:
            try:
                destination[key] = destination[key] | set(value)
            except (KeyError):
                destination[key] = value
        else:
            destination[key] = value
    return destination


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def rank_sources(src=None):
    """Create sources by stripping source info."""
    if src is None:
        srcs = glob.glob("carbonation/resources/articles/*.json")
    else:
        srcs = [src]

    try:
        with open("carbonation/resources/sources/nc_sources.json", "r") as f:
            nc_sources = json.load(f)
    except FileNotFoundError:
        nc_sources = {}

    # Go through articles and add
    for fn in srcs:
        with open(fn, "r") as f:
            articles = json.load(f)["articles"]

        to_write = {
            artcl["clean_url"]: {
                "rights": set([artcl["rights"]]),
                "rank": artcl["rank"],
                "country": artcl["country"],
                "language": artcl["language"],
                "twitter_account": set([artcl["twitter_account"]]),
            }
            for artcl in articles
        }

        print(len(to_write))

        nc_sources = merge(nc_sources, to_write)

    print("Done!", len(nc_sources))

    # At the end let's sort and write
    nc_sources = dict(sorted(nc_sources.items(), key=lambda x: x[1]["rank"]))

    with open("carbonation/resources/sources/nc_sources.json", "w") as f:
        json.dump(nc_sources, f, cls=SetEncoder)
