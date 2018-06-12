# meh-bot

A bot that clicks the spinner on Meh and sends a text message to user
First create a file called .env that contains 6 variables:
```
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_TO_NUMBER=...
TWILIO_FROM_NUMBER=...
MEH_USER=...
MEH_PASS=...
```
To just use the script:
```
python3 bot.py (I haven't tested on Python 2 but theoretically it should work)
```
To build the container on a server so it texts you at midnight:
```
docker build . -t meh-bot
docker run --name meh-bot meh-bot
```
That's it!
