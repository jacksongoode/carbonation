import gc
import json
from datetime import datetime

from huey import crontab

from app import huey

from .model import bert_model
from .process import fetch_store


@huey.periodic_task(crontab(minute=0, hour="*/4"))
def cron_gen_bert():
    model, topic_docs, news = generate_bert()

    # Cleanup?
    del model, topic_docs, news
    gc.collect()


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

    return model, topic_docs, news
