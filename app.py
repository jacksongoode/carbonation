import argparse
import json
import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from flask_assets import Bundle, Environment
from flask_compress import Compress
from newsapi import NewsApiClient
from newscatcherapi import NewsCatcherApiClient

from analysis import generate_bert
from utils import get_newsapi, get_newscatcher_headlines, split_url

# set configuration values
load_dotenv()
catcher = NewsCatcherApiClient(x_api_key=os.environ.get("NEWSCATCHER"))
newsapi = NewsApiClient(api_key=os.environ.get("NEWSAPI"))


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
assets = Environment(app)

sass = Bundle(
    "sass/custom/reset.sass",
    "sass/pico/pico.scss",
    "sass/custom/user.sass",
    filters="libsass",
    output="css/style.css",
)
assets.register("sass_all", sass)

app.jinja_env.globals.update(split_url=split_url)
app.config.from_object(Config())
Compress(app)

# Initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)

# Routing
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
    model_fn = "bert_test.json"
    with open(f"resources/computed/{model_fn}", "r") as f:
        news = json.load(f)

    return render_template("bubble.html", data=news)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(prog="carbonation", description="Make news!")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    if not args.debug:
        print("Starting scheduler!")
        scheduler.start()
        scheduler.add_job(
            id="generate_bert",
            func=generate_bert,
            trigger="interval",
            hours=4,
        )
    app.run(
        host="0.0.0.0",
        debug=args.debug,
        use_reloader=args.debug,
        port=os.getenv("PORT", default=5000),
    )
