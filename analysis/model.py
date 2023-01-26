import json
from urllib.parse import urlparse

from bertopic import BERTopic
# from hdbscan import HDBSCAN

# from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
# from umap import UMAP

news_json = "newscatcher_4hr_11-21-2022_02:02:51.json"


# def preprocess(docs):
#     cleaned_docs = [preprocess_string(d, CUSTOM_FILTERS) for d in docs]
#     cleaned_docs = [[lemmatizer.lemmatize(s) for s in t] for t in cleaned_docs]

#     return cleaned_docs


def bert_model(news=None):
    vectorizer_model = CountVectorizer(
        ngram_range=(1, 2), strip_accents="ascii", stop_words="english"
    )
    # embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    # umap_model = UMAP(n_neighbors=5, n_components=15)
    # hdbscan_model = HDBSCAN(gen_min_span_tree=True, prediction_data=True)

    model = BERTopic(
        # hdbscan_model=hdbscan_model,
        # embedding_model=embedding_model,
        # umap_model=umap_model,
        vectorizer_model=vectorizer_model,
        top_n_words=10,
        language="english",
        calculate_probabilities=True,
        verbose=True,
    )

    if news is None:
        with open(f"resources/articles/{news_json}", "r") as f:
            news = json.load(f)

    # Enrich docs with bias
    news = enrich_docs(news)

    docs = []
    links = []
    for a in news["articles"]:
        if a["excerpt"] is not None:
            docs.append(": ".join([a["title"], a["excerpt"]]))
            links.append(
                {"domain": a["clean_url"], "link": a["link"], "bias": a["bias"]}
            )

    # Remove dupes
    # docs = list(set(docs))
    # docs = preprocess(docs)

    # Make model
    topics, probs = model.fit_transform(docs)

    # Make resultant json
    model, topic_docs = create_topic_docs(model, topics, probs, docs, links)

    return (model, topic_docs)


def create_topic_docs(model, topics, probs, docs, links):
    topic_docs = {
        topic: {"topic": model.get_topic(topic), "docs": []} for topic in set(topics)
    }

    for topic, doc, prob, link in zip(topics, docs, probs, links):
        if max(prob) > 0.25:
            topic_docs[topic]["docs"].append(
                {"text": doc, "prob": sorted(prob.tolist())[-5:][::-1], **link}
            )

    for topic, content in topic_docs.items():
        num_docs = len(content["docs"])
        topic_docs[topic]["num_docs"] = num_docs
        topic_docs[topic]["avg_bias"] = 0

        if num_docs > 0:
            avg_bias = sum([doc["bias"] for doc in content["docs"]]) / num_docs
            topic_docs[topic]["avg_bias"] = avg_bias

    # topic_docs = sorted(topic_docs, key=lambda x: len(topic_docs[x]['docs']))

    # f"resources/computed/bert_{'_'.join(news_json.split('_')[1:])}", "w"
    with open("resources/computed/bert_test.json", "w") as f:
        f.write(json.dumps(topic_docs))

    return (model, topic_docs)


def enrich_docs(news):
    # news = json.load(open(f"resources/articles/{news_json}"))

    with open("resources/bias/mbfc_bias.json", "r") as f:
        mbfc_bias = json.load(f)

    mbfc_bias = {k: v["b"] for (k, v) in mbfc_bias.items()}

    with open("resources/bias/allsides_bias.json", "r") as f:
        allsides_bias = json.load(f)["allsides_media_bias_ratings"]

    # For AllSides compose dict
    allsides_bias = {
        ".".join(urlparse(s["source_url"]).netloc.split(".")[-2:]): s[
            "media_bias_rating"
        ]
        for s in allsides_bias
        if s["source_url"] != ""
    }

    bias = mbfc_bias | allsides_bias

    bias_scale = {
        # "CP": "Conspiracy-Pseudoscience",
        # "FN": "Questionable Sources",
        # "PS": "Pro-Science",
        # "S": "Satire",
        "L": -1,
        "Left": -1,
        "LC": -0.5,
        "Lean Left": -0.5,
        "C": 0,
        "Center": 0,
        "Mixed": 0,
        "RC": 0.5,
        "Lean Right": 0.5,
        "R": 1,
        "Right": 1,
    }

    for a in news["articles"]:
        a["bias"] = 0

        domain = a.get("clean_url", "")
        if domain in bias:
            a["bias"] = bias_scale.get(bias[domain], 0)

    return news
