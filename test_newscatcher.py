import json

from newscatcherapi import NewsCatcherApiClient

newscatcherapi = NewsCatcherApiClient(
    x_api_key='b_Gopvrwzl8fDrtDn-z__6jY1eAvUJ-Zk8lhstwb1UM')

if __name__ == "__main__":
    all_articles = newscatcherapi.get_search(q='Elon Musk',
                                             lang='en',
                                             countries='CA',
                                             page_size=100)
    for a in all_articles['articles']:
        print(a)
