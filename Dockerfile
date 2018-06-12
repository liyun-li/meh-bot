FROM python:3.6.5-alpine

RUN mkdir /meh-bot
WORKDIR /meh-bot
COPY * ./

RUN apk --update add firefox
RUN pip install -r req.txt

CMD python bot.py
