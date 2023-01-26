import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from huey.contrib.mini import MiniHuey
from newsapi import NewsApiClient
from newscatcherapi import NewsCatcherApiClient

from utils import get_newsapi, get_newscatcher_headlines

huey = MiniHuey()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Hot reload
if _debug := os.getenv("DEBUG"):
    import arel

    hot_reload = arel.HotReload(
        paths=[
            arel.Path("./static"),
            arel.Path("./templates"),
            arel.Path("./utils"),
            arel.Path("./resources"),
            arel.Path("./analysis"),
            arel.Path("main.py"),
        ],
    )
    app.add_websocket_route("/hot-reload", route=hot_reload, name="hot-reload")
    app.add_event_handler("startup", hot_reload.startup)
    app.add_event_handler("shutdown", hot_reload.shutdown)
    templates.env.globals["DEBUG"] = _debug
    templates.env.globals["hot_reload"] = hot_reload


# Set configuration values
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
