# carbonation

## Why?

At a glance, carbonation uses NLP to do topic modelling over the current news by grouping similar
articles based on headlines (and summaries if available!) and provide topics with bias ratings.
carbonation allows a reader to get an immediate sense of the current news and allows one to learn
which topics are covered more often by progressive or conservative outlets.

## How?

It does so by leveraging the [NewsCatcher API](https://newscatcherapi.com/) to retrieve articles and
summaries from the most popular news publishers.

Built with Flask, Next.js, and serverless Postgres.
