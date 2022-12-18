import json

from .model import bert_model
from .process import fetch_store


def generate_bert(hours=4, pages=10, news_json=None):
    print("Running bert gen job!")

    if news_json is None:
        news = fetch_store(hours=hours, max_page=pages)
        print("Successfully fetched news!")
    else:
        with open(news_json, "r") as f:
            news = json.load(f)

    model, topic_docs = bert_model(news)
    print("Successfully generated new model!")
    print(f"{len(topic_docs)} topics generated!")

    return
