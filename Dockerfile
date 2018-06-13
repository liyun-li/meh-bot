FROM fdsa/meh-bot

RUN mkdir /meh-bot
WORKDIR /meh-bot
COPY * ./

CMD python3 bot.py
