# Prerequisites

python requirements:

- discord.py==1.3.3
- PyNaCl==1.4.0

server requirement:

- ffmpeg

For linux `sudo apt-get install ffmpeg` would do.

discord requirements:

- an app
- a bot with it's token with at least channel management permissions.


# Running

Set up DISCORD_TOKEN as an environment variable

`source .env`

Then run the bot client

`python timer_bot.py`