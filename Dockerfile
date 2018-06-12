FROM python:3.6-alpine

RUN mkdir meh-bot
WORKDIR meh-bot
COPY * ./

RUN pip install -r req.txt
RUN /usr/bin/crontab crontab.txt

CMD /usr/sbin/crond -f -l 8
