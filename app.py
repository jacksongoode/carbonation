import json
import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from flask_compress import Compress
from newsapi import NewsApiClient
from newscatcherapi import NewsCatcherApiClient

from utils import get_newsapi, get_newscatcher_headlines, split_url

# set configuration values
load_dotenv()
catcher = NewsCatcherApiClient(x_api_key=os.environ.get("NEWSCATCHER"))
newsapi = NewsApiClient(api_key=os.environ.get("NEWSAPI"))


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.jinja_env.globals.update(split_url=split_url)
app.config.from_object(Config())
Compress(app)

# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)


@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/newsapi")
def render_newsapi():
    news = get_newsapi("*")
    data = {
        "articles": news["articles"],
        "total_results": news["totalResults"],
    }

    return render_template("newsapi.html", data=data)


@app.route("/newscatcher")
def render_newscatcher():
    news = get_newscatcher_headlines(1)
    data = {"articles": news.get("articles", ""), "total_results": news["total_hits"]}

    return render_template("newscatcher.html", data=data)


@app.route("/model")
def render_model():
    model_fn = "bert_4hr_11-05-2022_11:33:12.json"
    news = json.load(open(f"resources/computed/{model_fn}"))
    return render_template("bubble.html", data=news)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=os.getenv("PORT", default=5000))
