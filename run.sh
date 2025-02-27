#!/bin/bash

case $1 in
  dev)
    uv run uvicorn --host localhost --reload --reload-exclude='.trunk/' --reload-include='*.css' carbonation.main:app
    ;;
  dev-cron)
    uv run huey_consumer.py carbonation.main.huey &
    uv run uvicorn --host localhost --reload --reload-exclude='.trunk/' --reload-include='*.css' carbonation.main:app
    ;;
  prod)
    uv run setup.py build_sass && uv run huey_consumer.py carbonation.main.huey &
    uv run uvicorn --host 0.0.0.0 --port 8080 carbonation.main:app
    ;;
  railway)
    uv run setup.py build_sass && uv run huey_consumer.py carbonation.main.huey &
    uv run uvicorn --host 0.0.0.0 --port "$PORT" carbonation.main:app
    ;;
  *)
    echo -e "Unknown method!\nCall 'dev', 'prod', or 'railway'"
    ;;
esac