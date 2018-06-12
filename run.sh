#!/bin/bash

docker build . -t meh-bot
docker kill meh-bot 2>/dev/null
docker run --name meh-bot -d --rm meh-bot
