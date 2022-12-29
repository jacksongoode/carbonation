import json
from datetime import datetime

from huey import crontab

from app import huey

from .model import bert_model
from .process import fetch_store


@huey.periodic_task(crontab(minute=0, hour="*/4"))
def cron_gen_bert():
    generate_bert()


def generate_bert(hours=4, pages=10, news_json=None):
    print(f"Running bert gen job at {datetime.now()}")

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
