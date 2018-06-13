FROM fdsa/meh-bot:firefox

RUN mkdir /meh-bot
WORKDIR /meh-bot
COPY * ./

CMD python3 bot.py
