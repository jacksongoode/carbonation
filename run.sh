#!/bin/bash

case $1 in 
	dev)
		npm run sass-dev & uvicorn --reload --reload-include="*.css" main:app
		;;
	prod)
		npm run sass-prod && uvicorn --host 0.0.0.0 --port 8080 main:app
		;;
	railway)
		npm run sass-prod && uvicorn --host 0.0.0.0 --port $PORT main:app
		;;
	*)
		echo "Unknown method!"
		;;
esac 
