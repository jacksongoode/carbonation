from pprint import pprint

from newsapi import NewsApiClient
# Init
newsapi = NewsApiClient(api_key='5a3f0af6add84d15997ea15da457f2bf')

# /v2/top-headlines
if __name__ == "__main__":
    # top_headlines = newsapi.get_top_headlines(
    #     sources='al-jazeera-english, bbc-news',
    #     language='en')
    # pprint(top_headlines)

    # /v2/everything
    all_articles = newsapi.get_everything(q='bitcoin')

    pprint(all_articles)

    # # /v2/top-headlines/sources
    # sources = newsapi.get_sources()
    # pprint(sources)
