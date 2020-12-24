#!/usr/bin/python
# -*- coding: utf-8 -*-
import discord
import os
from discord.ext import commands 
import asyncio
import os
import datetime
import time
import aiohttp
from io import BytesIO
import json
import random
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''

changelogtext = """Version 1.1.5
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

commands_text = """Commands:
        * !fuck - flip the bird to anyone that annoys you
        * !info <user> - retrieves the profile information for a user
        * !commands - provides a list of all available commands
        * !uptime - shows how long the bot has been up for
        * !dazzyboo - makes the bot have a mental breakdown
        * !serious - the serious plea
        * !changelog - the changes since the last version"""

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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

ffmpeg_options = {
    'options': '-vn'
}

client = commands.Bot(command_prefix = '!')

start_time = datetime.datetime.now()

token = os.getenv('DISCORD_API_KEY', '')
giphy_token = os.getenv('GIPHY_API_KEY', '')
setFuck = None
middleFingerEmoji = '🖕'
hEmoji = '🇭'
oEmoji = '🇴'
rEmoji = '🇷'
sEmoji = '🇸'
eEmoji = '🇪'
dazzyRant = 'Hello folks. Sorry for the typos lads. What an eventful fucking night that was on Discord, then wakes up to aw that this morning. Anyway, Statement. For the last 2 months me n Caitlin have been chatting a lot as ye\'s know. And we\'ve even met up a few times. As some of yous know, I liked her a lot can ye believe it? I\'d even go as far as saying we were seeing each other. At one point we both acknowledged we both wanted to be a couple. Anyway, this last week or so has been a fuckin mind game to her. I made a daft decision at the start of whatever it was we\'ve been doing. I told her I wasnae involved in something that I was and I\'ve been getting punished a fucker. She\'s been using Stephen to get back at me. You see, there\'s been patter in here about her going on a date wi Stephen and it made me a wee bit insecure. It happens. So as punishment she\'s been playing wi him and chatting wi him and completely ignoring me. Then when I ask whats going on, she says nothing and not to worry and that we\'ll be fine and the she\'s right back on wi him. This has cause the last week or so of anxiety attacks and mental fuckin breakdowns. 3 times I\'ve tried to walk away from her and 3 times she\'s phoned me. Once to tell me I\'m an idiot and I\'m over thinking things. Once to tell me to stop playing games with folk without her (especially butters) and once because one of these cunts told her. I told them about us. I\'m no mad though. What I am mad about is the phone call I got last night from her. Where she told me that I wasn\'t to speak to anyone in the discord. She told me that, for my own well being I needed a break and for that reason I wasn\'t to reach out to anyone and if I did, she\'d find out. If I played games with anyone she\'d find out. If I appeared offline with someone, she\'d find out. Meanwhile telling me it\'s cause everyone cares. I couldnae really work out what was happening. '
dazzyRant2 = 'So naturally I jump up and I\'m on the discord to butters. Ignored. Then a text comes in from her asking why im messaging him. Then he messages me. Turns out folk aren\'t ignoring me cause they care it\'s because she\'s told some cunts, I don\'t know everyone, that I\'ve made all this shite up. I don\'t know how she\'s made it look either. If she\'s made me look pathetic and lonely or if I look like a psycho but I can absolutely assure yous she\'s manipulating the fuckin lot of us and she\'s loving it. I know most of yous probably don\'t care but this is what\'s happening behind the scenes. 2 folk I consider mates and have known for year, albeit I\'ve never met butters but still, have been turned against me cause they\'ve been convinced im lying about something. Have a nice day, I don\'t expect anycunt to take sides, im no a wean but it\'d be nice to have more folk in the know instead of her pretending in that discord that everythings fine and im outside feeling like shite cause wilky\'s the only cunt that wants to talk to me. She might flip this, tell yous im at it and im making shite up again. And yous might believe her cause she\'s a lassie but I can assure yous, she\'s a better liar than I am and I couldnae make something this fuckin childish and petty up if I tried. Hope to see all my gaming pals on Rainbow 6 now that I\'m free and allowed to play games myself again. God bless.'
seriousRant = 'Hello folks. This is a serious post so i\'m asking you to please read it. Some of yous willnae know but i was seeing someone for a wee while there. She turned out to be a psycho in the end, some folk know the details others dinnae need to. Well in the last few days i\'ve started getting death threats from random cunts. I\'ll no go into too much detail, but the wee cow has been telling folk online somewhere that i\'m a paedo. I dinnae know where, i dinnae know how many folk, i no nothing. Im wanting folk to know this cause if anyone gets a message, it\'s unlikely but if you do, please tell me, screenshot it, report it and then block them. I\'m taking any new information i get to the police. Thanks for reading. God bless'

godDictionary = {}

@client.event
async def on_ready():
    with open('/projects/discord-bots/vocab.dd') as file:
        i = 1
        for line in file:
            godDictionary[i] = line
            i = i + 1

    print ('No adventure is complete without Jingle hat and Jingle feet')        
    channel = client.get_channel(514244679907147776)
    global start_time
    start_time = datetime.datetime.now()
    await channel.send('ChairsBot started at: ' + start_time.strftime("%d/%m/%Y, %H:%M:%S"))

@client.event
async def on_message(message):
    if setFuck != None:
        if message.author.name == setFuck:
            await message.add_reaction(emoji=middleFingerEmoji)
    if 'horse' in message.content.lower():
        await message.add_reaction(emoji=hEmoji)
        await message.add_reaction(emoji=oEmoji)
        await message.add_reaction(emoji=rEmoji)
        await message.add_reaction(emoji=sEmoji)
        await message.add_reaction(emoji=eEmoji)
    await client.process_commands(message)

@client.command()
async def uptime(ctx):
    global start_time
    diff = datetime.datetime.now() - start_time
    time_diff = time.gmtime(diff.seconds)
    time_print = time.strftime("%H:%M:%S", time_diff)
    await ctx.send('I have been up for: ' + time_print)

@client.command()
async def commands(ctx):
    await ctx.send(commands_text)

@client.command()
async def changelog(ctx):
    await ctx.send(changelogtext)

@client.command()
async def fuck(ctx, *args):
    memberToCheck = ' '.join(args)
    global setFuck
    for member in ctx.message.guild.members:
        # print('[DEBUG]' + member.name)
        if (member.name.lower() == memberToCheck.lower() or (member.nick != None and member.nick.lower() == memberToCheck.lower())):
            await ctx.send('That\'s right, fuck ' + member.name)
            setFuck = member.name
            return 
        if (memberToCheck.lower() in member.name.lower() or (member.nick != None and memberToCheck.lower() in member.nick.lower())):
            if member.nick == None:
                await ctx.send('I\'m guessing you meant fuck ' + member.name + '. If you didn\'t - fuck them anyway!')
            else:
                await ctx.send('I\'m guessing you meant fuck ' + member.name + '/' + member.nick + '. If you didn\'t - fuck them anyway!')
            setFuck = member.name
            return 
    await ctx.send('Who the fuck is ' + memberToCheck + '?')
    setFuck = None

@client.command()
async def dazzyboo(ctx):
    await ctx.send(dazzyRant)
    await ctx.send(dazzyRant2)

@client.command()
async def serious(ctx):
    await ctx.send(seriousRant)

async def info(ctx, *args):
    memberToCheck = ' '.join(args)
    for member in ctx.message.guild.members:
        if (member.name.lower() == memberToCheck.lower()):
            info_text = """User Information:
            
            * Name: {}, 
            * ID: {} 
            * Discriminator: {}, 
            * Created at: {}, 
            * Avatar {}""".format(member.name, member.id, member.discriminator, member.created_at, member.avatar_url)
            
            await ctx.send(info_text)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@client.command()
async def stream(ctx, *, url):
    # url = "https://www.youtube.com/watch?v=oHg5SJYRHA0"
    # =ZcBNxuKZyN4
    url = "https://www.youtube.com/watch?v=" + url
    await ctx.send("Attempting to join voice channel")
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(ctx.author.voice.channel)
    else:
        await ctx.author.voice.channel.connect()
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    player = await YTDLSource.from_url(url, stream=True)
    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(player.title))

    await ctx.send("Leaving voice channel in 10s")
    await asyncio.sleep(10)
    await ctx.voice_client.disconnect()

@client.command()
async def music(ctx):
    await ctx.send("Attempting to join voice channel")
    if ctx.voice_client is not None:
        #await ctx.voice_client.move_to(ctx.author.voice.channel)
        await ctx.voice_client.disconnect()
        await ctx.author.voice.channel.connect()
    else:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

#source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("/projects/discord-bots/music.mp3"))

#source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("http://cdn-data.motu.com/media/ethno/demo-audio/mp3/Indian-Legatos-2.mp3"))

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("https://terrum.co.uk/uploads/1492101903.mp3"))

    ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

@client.command()
async def stop(ctx):
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect() 

@client.command()
async def god(ctx):
    words = ""
    for x in range(30):
        # Use os.urandom() to generate secure
        godSecure = random.SystemRandom().randint(1, 7569) # 7569 lines in dictionary
        words = words + godDictionary.get(godSecure).replace("\n", " ")
    await ctx.send(words)

async def checkKol():
    await client.wait_until_ready()
    print("KoL Poller has started")
    while(True):
        path = '/projects/completed/'
        prefixed = [filename for filename in os.listdir('/projects/completed/') if filename.startswith("kol")]
        for x in prefixed:
            todelete = path + x
            x = x.replace('kol-', '')
            x = x.replace('.log', '')
            date_time = datetime.datetime.strptime(x, '%Y%m%d%H%M%S')
            channel = client.get_channel(514244679907147776)
            await channel.send('KoL Cron Job successfully executed at: ' + date_time.strftime("%d/%m/%Y, %H:%M:%S"))
            os.remove(todelete)
        await asyncio.sleep(60) # task runs every 60s

async def dailyHorse():
    await client.wait_until_ready()
    print("Daily Horse has started")
    while(True):
        channel = client.get_channel(791301208756584469)
        red = random.SystemRandom().randint(1, 255)
        green = random.SystemRandom().randint(1, 255)
        blue = random.SystemRandom().randint(1, 255)        
        embed = discord.Embed(colour=discord.Colour.from_rgb(red, green, blue))
        session = aiohttp.ClientSession()    
        response = await session.get('https://api.giphy.com/v1/gifs/random?tag=horse&api_key=' + giphy_token)
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
        await channel.send('Enjoy your daily horse GIF - \'' + data['data']['title'] + '\' brought to you by: ' + data['data']['username'])
        await channel.send(embed=embed)
        await session.close()
        await asyncio.sleep(86400) # runs every 24 hours

#client.loop.create_task(dailyHorse())
client.loop.create_task(checkKol())
client.run(token)
