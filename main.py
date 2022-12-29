import uvicorn

# trunk-ignore(flake8/F401)
from analysis import cron_gen_bert
# trunk-ignore(flake8/F401)
from app import app, huey

if __name__ == "__main__":
    print("Starting!")
    uvicorn.run("main:app", port=8080, log_level="info")
