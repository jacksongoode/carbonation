from utils import *
from analysis import *

from gensim import corpora, models, similarities, downloader
from gensim.parsing.preprocessing import remove_stopwords, preprocess_documents
from gensim.test.utils import common_corpus, common_dictionary
from gensim.models import HdpModel, LdaModel, Nmf
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from collections import Counter

from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN

from gensim.parsing.preprocessing import *

news_json = 'newscatcher_4hr_11-05-2022_11:33:12.json'
CUSTOM_FILTERS = [lambda x: x.lower(), strip_tags, strip_punctuation,
                  strip_multiple_whitespaces, remove_stopwords, strip_short]


def preprocess(docs):
    cleaned_docs = [preprocess_string(d, CUSTOM_FILTERS) for d in docs]
    # cleaned_docs = [[lemmatizer.lemmatize(s) for s in t] for t in cleaned_docs]

    return cleaned_docs


def bert_model():
    vectorizer_model = CountVectorizer(
        ngram_range=(
            1, 2), strip_accents='ascii',
        stop_words="english")
    embedding_model = SentenceTransformer(
        'sentence-transformers/all-MiniLM-L6-v2')
    # umap_model = UMAP(n_neighbors=5, n_components=15)
    hdbscan_model = HDBSCAN(gen_min_span_tree=True,
                            prediction_data=True)

    model = BERTopic(
        hdbscan_model=hdbscan_model,
        embedding_model=embedding_model,
        # umap_model=umap_model,
        vectorizer_model=vectorizer_model,
        top_n_words=10,
        language='english',
        calculate_probabilities=True,
        verbose=True
    )
    news = json.load(open(f'resources/articles/{news_json}'))

    docs = []
    links = []
    for a in news['articles']:
        if a['excerpt'] is not None:
            docs.append(': '.join([a['title'], a['excerpt']]))
            links.append({'author': a['clean_url'], 'url': a['link']})

    # Remove dupes
    # docs = list(set(docs))
    # docs = preprocess(docs)

    topics, probs = model.fit_transform(docs)
    model, topic_docs = create_topic_docs(model, topics, probs, docs, links)

    return (model, topic_docs)


def create_topic_docs(model, topics, probs, docs, links):
    topic_docs = {topic: {"topic": model.get_topic(topic), "docs": []}
                  for topic in set(topics)}

    for topic, doc, prob, link in zip(topics, docs, probs, links):
        if max(prob) > 0.5:
            topic_docs[topic]["docs"].append(
                {"text": doc,
                 "prob": sorted(prob.tolist())[-5:][::-1],
                 **link}
            )

    with open(f"resources/computed/bert_{'_'.join(news_json.split('_')[1:])}", "w") as f:
        f.write(json.dumps(topic_docs))

    return (model, topic_docs)
