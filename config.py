#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

### Version and changelog information
version = "1.1.6"
changelog = """Version 1.1.6
        * Various code clean-up tasks
        * Renamed !commands to !help to stop overriding of Discord import 

Version 1.1.5
        * Resolved issues with bot changing channel

Version 1.1.4
        * Added ability to stream audio YouTube using !stream
        * Added mechanism to stream local mp3s

Version 1.1.3
        * Added daily horse gif retrieval from Giphy
        * Added H O R S E emojis whenever horse is mentioned in a sentence
        * Added random colour to embedded horse
        * Added port of God from TempleOS converted crudely from HolyC to Python

Version 1.1.2
        * Externalised token to environment variable
        * Updated uptime to be more human readable

Version 1.1.1
        * Resolved polling issue with cron job notifications

Version 1.1.0
        * Restored ChairsBot and rotated token
        * Updated discord.py to 1.4.1
        * Removed broken Twitch polling (API change)
        * Removed !tomato command
        * Removed !echo command
        * Removed !argtest command
        * Added !changelog command
        * Added automatic cron job update in #dev-test
        * Added !uptime command
        * Added !commands command
        * Renamed !getInfo command to !info
        * Improved !info formatting

Version 1.0.0       
        * First pass of info, fuck, dazzyboo and serious commands
        * Integrated Twitch API poller"""

### List of commands
commands = """Commands:
        * !fuck - flip the bird to anyone that annoys you
        * !info <user> - retrieves the profile information for a user
        * !help - provides a list of all available commands
        * !uptime - shows how long the bot has been up for
        * !dazzyboo - makes the bot have a mental breakdown
        * !serious - the serious plea
        * !changelog - the changes since the last version"""

### YouTube Downloader 
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

### FFmpeg configuration 
ffmpeg_options = {
    'options': '-vn'
}

### Environment variables 
discord_api_key = os.getenv('DISCORD_API_KEY', '')
giphy_api_key = os.getenv('GIPHY_API_KEY', '')


### God dictionary configuration
vocabulary = "vocab.dd"
god_dictionary = {}
# Loads the God dictionary into memory, currently this is 7569 words
with open(vocabulary) as file:
    i = 1
    for line in file:
        god_dictionary[i] = line
        i = i + 1

### Discord channels
class Discord:
    dev_test = 514244679907147776
    daily_horse = 791301208756584469

### Static text fields
dazzy_rant = 'Hello folks. Sorry for the typos lads. What an eventful fucking night that was on Discord, then wakes up to aw that this morning. Anyway, Statement. For the last 2 months me n Caitlin have been chatting a lot as ye\'s know. And we\'ve even met up a few times. As some of yous know, I liked her a lot can ye believe it? I\'d even go as far as saying we were seeing each other. At one point we both acknowledged we both wanted to be a couple. Anyway, this last week or so has been a fuckin mind game to her. I made a daft decision at the start of whatever it was we\'ve been doing. I told her I wasnae involved in something that I was and I\'ve been getting punished a fucker. She\'s been using Stephen to get back at me. You see, there\'s been patter in here about her going on a date wi Stephen and it made me a wee bit insecure. It happens. So as punishment she\'s been playing wi him and chatting wi him and completely ignoring me. Then when I ask whats going on, she says nothing and not to worry and that we\'ll be fine and the she\'s right back on wi him. This has cause the last week or so of anxiety attacks and mental fuckin breakdowns. 3 times I\'ve tried to walk away from her and 3 times she\'s phoned me. Once to tell me I\'m an idiot and I\'m over thinking things. Once to tell me to stop playing games with folk without her (especially butters) and once because one of these cunts told her. I told them about us. I\'m no mad though. What I am mad about is the phone call I got last night from her. Where she told me that I wasn\'t to speak to anyone in the discord. She told me that, for my own well being I needed a break and for that reason I wasn\'t to reach out to anyone and if I did, she\'d find out. If I played games with anyone she\'d find out. If I appeared offline with someone, she\'d find out. Meanwhile telling me it\'s cause everyone cares. I couldnae really work out what was happening. '
dazzy_rant_2 = 'So naturally I jump up and I\'m on the discord to butters. Ignored. Then a text comes in from her asking why im messaging him. Then he messages me. Turns out folk aren\'t ignoring me cause they care it\'s because she\'s told some cunts, I don\'t know everyone, that I\'ve made all this shite up. I don\'t know how she\'s made it look either. If she\'s made me look pathetic and lonely or if I look like a psycho but I can absolutely assure yous she\'s manipulating the fuckin lot of us and she\'s loving it. I know most of yous probably don\'t care but this is what\'s happening behind the scenes. 2 folk I consider mates and have known for year, albeit I\'ve never met butters but still, have been turned against me cause they\'ve been convinced im lying about something. Have a nice day, I don\'t expect anycunt to take sides, im no a wean but it\'d be nice to have more folk in the know instead of her pretending in that discord that everythings fine and im outside feeling like shite cause wilky\'s the only cunt that wants to talk to me. She might flip this, tell yous im at it and im making shite up again. And yous might believe her cause she\'s a lassie but I can assure yous, she\'s a better liar than I am and I couldnae make something this fuckin childish and petty up if I tried. Hope to see all my gaming pals on Rainbow 6 now that I\'m free and allowed to play games myself again. God bless.'
serious_rant = 'Hello folks. This is a serious post so i\'m asking you to please read it. Some of yous willnae know but i was seeing someone for a wee while there. She turned out to be a psycho in the end, some folk know the details others dinnae need to. Well in the last few days i\'ve started getting death threats from random cunts. I\'ll no go into too much detail, but the wee cow has been telling folk online somewhere that i\'m a paedo. I dinnae know where, i dinnae know how many folk, i no nothing. Im wanting folk to know this cause if anyone gets a message, it\'s unlikely but if you do, please tell me, screenshot it, report it and then block them. I\'m taking any new information i get to the police. Thanks for reading. God bless'
### Emojis 
class Emoji:
    middle_finger = '🖕'
    regional_indicator_h = '🇭'
    regional_indicator_o = '🇴'
    regional_indicator_r = '🇷'
    regional_indicator_s = '🇸'
    regional_indicator_e = '🇪'
