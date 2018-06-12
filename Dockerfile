FROM python:3.6.5-slim-stretch

RUN mkdir /opt/meh-bot
WORKDIR /opt/meh-bot
COPY * ./

RUN apt-get update && apt-get -y install firefox
RUN pip install -r req.txt

CMD python bot.py
