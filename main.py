import argparse
import json
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from newsapi import NewsApiClient
from newscatcherapi import NewsCatcherApiClient

from utils import get_newsapi, get_newscatcher_headlines, split_url

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# app.jinja_env.globals.update(split_url=split_url)

# set configuration values
load_dotenv()
catcher = NewsCatcherApiClient(x_api_key=os.environ.get("NEWSCATCHER"))
newsapi = NewsApiClient(api_key=os.environ.get("NEWSAPI"))

# Routing
@app.get("/", response_class=HTMLResponse)
@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/newsapi", response_class=HTMLResponse)
def render_newsapi(request: Request):
    news = get_newsapi("*")
    data = {
        "articles": news["articles"],
        "total_results": news["totalResults"],
    }

    return templates.TemplateResponse(
        "newsapi.html", {"request": request, "data": data}
    )


@app.get("/newscatcher", response_class=HTMLResponse)
def render_newscatcher(request: Request):
    news = get_newscatcher_headlines(1)
    data = {"articles": news.get("articles", ""), "total_results": news["total_hits"]}

    return templates.TemplateResponse(
        "newscatcher.html", {"request": request, "data": data}
    )


@app.get("/model", response_class=HTMLResponse)
def render_model(request: Request):
    model_fn = "bert_test.json"
    with open(f"resources/computed/{model_fn}", "r") as f:
        data = json.load(f)

    return templates.TemplateResponse("bubble.html", {"request": request, "data": data})


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(prog="carbonation", description="Make news!")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    # if not args.debug:
    #     from analysis import generate_bert

    #     print("Starting scheduler!")
    #     scheduler.start()
    #     scheduler.add_job(
    #         id="generate_bert",
    #         func=generate_bert,
    #         trigger="interval",
    #         hours=4,
    #     )

    print("Starting!")
    uvicorn.run("main:app", port=8080, log_level="info")
