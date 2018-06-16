#!/bin/bash

docker build . -t meh-bot --no-cache
docker rm -f meh-bot 2>/dev/null
docker run --name meh-bot -d -t meh-bot
echo 'Meh bot is running. Go do whatever'
