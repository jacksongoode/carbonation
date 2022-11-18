from .model import bert_model
from .process import fetch_store


def generate_bert():
    print("Running bert gen job!")

    news = fetch_store(4)
    print("Successfully fetched news!")

    model, topic_docs = bert_model(news)
    print("Successfully generated new model!")

    print(f"{len(topic_docs)} topics generated!")
