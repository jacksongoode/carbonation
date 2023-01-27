
from datetime import datetime
import json

# import sys, os
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'carbonation'))
from ..analysis import bert_model, fetch_store


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


if __name__ == "__main__":
    generate_bert()
