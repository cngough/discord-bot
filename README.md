# discord-bot
Multiple Discord experiments powered by [discord.py](https://discordpy.readthedocs.io/en/latest/api.html).  

## Pre-requisites
The following Python 3 dependencies must be installed before running (install using `pip3 install -U <library>`):  
- aiohttp 3.6.3  
- asyncio 3.4.3  
- discord.py[voice] 1.5.1  
- youtube-dl 2020.12.26   
  
The following environment variables must be configured in the running environment:  
- `DISCORD_BOT_API_KEY` - A bot token gained by registering a bot on https://www.discord.com/developers/applications  
- `GIPHY_API_KEY` - A beta or production API key from https://developers.giphy.com  

## Running 
The bot can be run by executing `python3 discord-bot.py` in a command line window.

## Commands
`!flip <user>` - indefinitely adds a middle finger emoji to a target user  
`!info <user>` - retrieves the profile information of a target user  
`!uptime` - displays the uptime of the bot in the current channel  
`!dazzyboo` - displays a rant in the current channel  
`!serious` - displays a plea in the current channel  
`!changelog` - displays all relevant changes  
`!music` - plays music in the voice channel the requesting user is in  
`!stream <youtube id>` - streams audio from youtube to the voice channel the requesting user is in  
`!husky` - retrieves a random husky from giphy in the current channel  
`!thanks` - replaces a word with a thankified version  
`!help` - displays a list of permitted commands  
