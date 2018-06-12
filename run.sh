#!/bin/bash

docker build . -t meh-bot
docker kill meh-bot && docker rm meh-bot 2>/dev/null
docker run --name meh-bot -d meh-bot
echo 'Meh bot is running. Go do whatever'
