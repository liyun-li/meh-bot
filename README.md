# meh-bot
A bot that clicks the spinner on Meh and optionally sends a text message to user about their product.

## Requirement
You need Python and Twilio service if you want to send a text to your phone (which is just a title and a picture). 
You also need Docker if you want to containerize the bot. 

## Getting Started
First create a .env file that contains 6 variables.

* Assign anything other than empty string to ``DO_THIS_EVERY_DAY`` if you want it to run every day
* Assign anything other than empty string to ``SEND_SMS`` if you want to activate texting
* If you choose to activate texting, learn the basics of Twilio and you should be able to fill out ``ACCOUNT_SID`` and ``AUTH_TOKEN``
* ``TWILIO_TO_NUMBER`` and ``TWILIO_FROM_NUMBER`` are the receiver and sender respectively
* ``MEH_USER`` could be your email address or username
```
DO_THIS_EVERY_DAY=...
SEND_SMS=...
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_TO_NUMBER=...
TWILIO_FROM_NUMBER=...
MEH_USER=...
MEH_PASS=...
```
To use the script locally:
```shell
python3 bot.py
```
To build a Docker container on a server:
```shell
./run.sh # OR
sh ./run.sh
```
That's it!
