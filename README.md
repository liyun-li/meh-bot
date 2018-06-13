# Meh Bot
A Python bot that clicks the daily Meh icon and optionally sends a text message to consumer about their product.

## Sales Pitch
If you subscribe to Meh, you'd think "Wouldn't it be great if I could check this website every day???", but then you always forget about the site because you're so occupied with other stuff? Well here you go! An automated bot that texts you about your Meh product and clicks the flipper for you so you don't have to visit the site on your own! Meh Bot, your personal clicking assistant. Download now!

## Requirement
First You need Python. You also need a Twilio account if you want to send product info to your phone (which is just a title and a picture). You also need Docker to containerize the app.

If you hate Docker, use Ubuntu. Bot is only tested on Xenial and Artful. 

## Getting Started
First create a file called ``.env``. _The program won't work without it._

* Assign anything other than an empty string to ``DO_THIS_EVERY_DAY`` if you want it to run every day
* Assign anything other than an empty string to ``RUN_IT_ONCE`` if you want it once before countdown starts
* Assign anything other than an empty string to ``SEND_SMS`` if you want to activate texting
* If you choose to activate texting, learn the basics of Twilio and you should be able to fill out ``ACCOUNT_SID`` and ``AUTH_TOKEN``
* ``TWILIO_TO_NUMBER`` and ``TWILIO_FROM_NUMBER`` are the receiver and sender respectively
* ``MEH_USER`` could be your email address or username
* ``MEH_PASS`` is the plain-text string you post on GitHub like everyone else
```
DO_THIS_EVERY_DAY=...
SEND_SMS=...
RUN_IT_ONCE=...
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_TO_NUMBER=...
TWILIO_FROM_NUMBER=...
MEH_USER=...
MEH_PASS=...
```
To use the script locally:
```shell
# Theoretically it should work on Python 2
apt-get update && apt-get install firefox # chromium and chrome support coming soon!
pip3 install -r req.txt
python3 bot.py
```
To build a Docker container on a server:
```shell
sh ./run-fg.sh # foreground, best run on tmux or equivalent
# OR
sh ./run-bg.sh # daemon task
```
That's it!

## Issues
* Help I can't get Chrome and Chromium to work with Selenium.
* I was told my code looks messy??? Help!

## Paradox
It's funny because after making Meh Bot I actually went and check Meh every day now. Nevertheless, Meh has earned my loyalty. Maybe they should hire me.
