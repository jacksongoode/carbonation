import json
import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from huey import SqliteHuey

from carbonation.utils import get_newsapi, get_newscatcher_headlines

huey = SqliteHuey(filename="/tmp/queue.db")

app = FastAPI()
app.mount("/static", StaticFiles(directory="carbonation/static"), name="static")
templates = Jinja2Templates(directory="carbonation/templates")

# Hot reload
if _debug := os.getenv("DEBUG"):
    import arel

    hot_reload = arel.HotReload(
        paths=[
            arel.Path("carbonation/static"),
            arel.Path("carbonation/templates"),
            arel.Path("carbonation/utils"),
            arel.Path("carbonation/resources"),
            arel.Path("carbonation/analysis"),
            arel.Path("carbonation/main.py"),
        ],
    )
    app.add_websocket_route("/hot-reload", route=hot_reload, name="hot-reload")
    app.add_event_handler("startup", hot_reload.startup)
    app.add_event_handler("shutdown", hot_reload.shutdown)
    templates.env.globals["DEBUG"] = _debug
    templates.env.globals["hot_reload"] = hot_reload


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
    with open(f"carbonation/resources/computed/{model_fn}", "r") as f:
        data = json.load(f)

    return templates.TemplateResponse("bubble.html", {"request": request, "data": data})
