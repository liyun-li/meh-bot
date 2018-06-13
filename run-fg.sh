#!/bin/bash

docker build . -t meh-bot
docker rm -f meh-bot 2>/dev/null
docker run --name meh-bot -ti meh-bot
echo 'Meh bot is running. Go do whatever'
