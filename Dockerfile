FROM spacebar2/python-selenium

RUN mkdir /meh-bot
WORKDIR /meh-bot
COPY * ./

RUN pip3 install -r req.txt

CMD python3 bot.py
