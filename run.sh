#!/bin/bash

case $1 in 
	dev)
		npm run sass-dev & uvicorn --reload --reload-include="*.css" main:app
		;;
	prod)
		npm run sass-prod
		;;
	*)
		echo "Unknown method!"
		;;
esac 
