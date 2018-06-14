#!/bin/bash

docker build . -t meh-bot --no-cache
docker rm -f meh-bot 2>/dev/null
docker run --name meh-bot -ti meh-bot
