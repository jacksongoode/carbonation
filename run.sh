#!/bin/bash

case $1 in
dev)
	npm run sass-dev &
	DEBUG=true uvicorn --reload --reload-exclude=".trunk/" --reload-include="*.css" carbonation.main:app
	;;
prod)
	npm run sass-prod && huey_consumer.py carbonation.main.huey &
	uvicorn --host 0.0.0.0 --port 8080 carbonation.main:app
	;;
railway)
	npm run sass-prod && huey_consumer.py main.huey &
	uvicorn --host 0.0.0.0 --port "$PORT" carbonation.main:app
	;;
*)
	echo -e "Unknown method!\nCall 'dev', 'prod', or 'railway'"
	;;
esac
