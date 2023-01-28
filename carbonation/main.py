import uvicorn

# trunk-ignore(flake8/F401)
from carbonation.app import app, huey

# trunk-ignore(flake8/F401)
from carbonation.jobs import cron_gen_bert

if __name__ == "__main__":
    print("Starting!")
    uvicorn.run("main:app", port=8080, log_level="info")
