#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import datetime
import json
import os
import random
import time
from io import BytesIO

import aiohttp
import discord
import youtube_dl
from discord.ext import commands

import config

# Global variables
intents = discord.Intents(messages=True, guilds=True, members=True)
ytdl = youtube_dl.YoutubeDL(config.YTDL_FORMAT_OPTIONS)
youtube_dl.utils.bug_reports_message = lambda: ''
client = commands.Bot(command_prefix='!', intents=intents)
start_time = datetime.datetime.now()
react_with_flip = None


@client.event
async def on_ready():
    print(config.ON_READY)
    channel = client.get_channel(config.Discord.DEV_TEST)
    global start_time
    start_time = datetime.datetime.now()
    await channel.send("ChairsBot started at: {}".format(start_time.strftime('%d/%m/%Y, %H:%M:%S')))

# Task - Why don't we add H O R S E into a list or enumeration and then iterate over that. Looks like it would be a bit neater? 
@client.event
async def on_message(message):
    if react_with_flip != None:
        if message.author.name == react_with_flip:
            await message.add_reaction(emoji=config.Emoji.MIDDLE_FINGER)
    if 'horse' in message.content.lower():
        await message.add_reaction(emoji=config.Emoji.REGIONAL_INDICATOR_H)
        await message.add_reaction(emoji=config.Emoji.REGIONAL_INDICATOR_O)
        await message.add_reaction(emoji=config.Emoji.REGIONAL_INDICATOR_R)
        await message.add_reaction(emoji=config.Emoji.REGIONAL_INDICATOR_S)
        await message.add_reaction(emoji=config.Emoji.REGIONAL_INDICATOR_E)
        # Might as well add a heart emoji here too, or a thumbs up
    await client.process_commands(message)

# Task - We can probably make this a bit more pythonic, using a lot of variables where fewer might be clearer
@client.command()
async def uptime(ctx):
    global start_time
    diff = datetime.datetime.now() - start_time
    time_diff = time.gmtime(diff.seconds)
    time_print = time.strftime('%H:%M:%S', time_diff)
    await ctx.send("I have been up for: {}".format(time_print))


@client.command()
async def actions(ctx):
    await ctx.send(config.COMMANDS)


@client.command()
async def changelog(ctx):
    await ctx.send(config.CHANGELOG)

# Task - The logic on 78 isn't doing anything. Let's wrap this in tests. 
@client.command()
async def flip(ctx, *args):
    member_to_check = ' '.join(args)
    global react_with_flip
    for member in ctx.message.guild.members:
        if (member.name.lower() == member_to_check.lower() or (member.nick != None and member.nick.lower() == member_to_check.lower())):
            await ctx.send("That's right, flip {}".format(member.name))
            react_with_flip = member.name
            return
        if (member_to_check.lower() in member.name.lower() or (member.nick != None and member_to_check.lower() in member.nick.lower())):
            # Are we actually doing anything with this logic?
            if member.nick == None:
                await ctx.send("I'm guessing you meant say flip {}. If you didn't - flip them anyway!".format(member.name))
            else:
                await ctx.send("I'm guessing you meant say flip {}/{}. If you didn't - flip them anyway!".format(member.name, member.nick))
            react_with_flip = member.name
            return
    await ctx.send("Who the flip is {}?".format(member_to_check))
    react_with_flip = None

# Maybe for simple send() commands have a message sending method that takes args and sends them in order. async def sendToChannel(ctx, *args) and iterate over the list
@client.command()
async def dazzyboo(ctx):
    await ctx.send(config.DAZZY_RANT)
    await ctx.send(config.DAZZY_RANT_2)


@client.command()
async def serious(ctx):
    await ctx.send(config.SERIOUS_RANT)

@client.command()
async def info(ctx, *args):
    member_to_check = ' '.join(args)
    for member in ctx.message.guild.members:
        if (member.name.lower() == member_to_check.lower()):
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
        return cls(discord.FFmpegPCMAudio(filename, **config.FFMPEG_OPTIONS), data=data)

# Task - Remove timeout for testing. Maybe consider getting length of YouTube URL. 
@client.command()
async def stream(ctx, *, url):
    if url == None:
        await ctx.send("Format is !stream [video_id]")
        return

    url = "https://www.youtube.com/watch?v={}".format(url)
    await ctx.send("Attempting to join voice channel")
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(ctx.author.voice.channel)
    else:
        await ctx.author.voice.channel.connect()
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    player = await YTDLSource.from_url(url, stream=True)
    ctx.voice_client.play(player, after=lambda e: print(
        'Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(player.title))

    await ctx.send("Leaving voice channel in 10s")
    await asyncio.sleep(10)
    await ctx.voice_client.disconnect()

# Task - Parameterise/externalise MP3s. Return a list in chat tied to an enumeration of whitelisted songs?
@client.command()
async def music(ctx):
    await ctx.send("Attempting to join voice channel")
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.author.voice.channel.connect()
    else:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError(
                "Author not connected to a voice channel.")
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(
        "https://terrum.co.uk/uploads/1492101903.mp3"))

    ctx.voice_client.play(source, after=lambda e: print(
        'Player error: %s' % e) if e else None)


@client.command()
async def stop(ctx):
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()


@client.command()
async def god(ctx):
    words = ""
    for _ in range(30):
        # Use os.urandom() to generate secure
        godSecure = random.SystemRandom().randint(1, 7569)  # 7569 lines in dictionary
        words = words + config.GOD_DICTIONARY.get(godSecure).replace("\n", " ")
    await ctx.send(words)

# Task - Externalise folder location. Remove string replacements with regex
async def check_kol():
    await client.wait_until_ready()
    print("KoL Poller has started")
    while(True):
        path = '/projects/completed/'
        prefixed = [filename for filename in os.listdir(
            '/projects/completed/') if filename.startswith("kol")]
        for x in prefixed:
            todelete = path + x
            x = x.replace('kol-', '')
            x = x.replace('.log', '')
            date_time = datetime.datetime.strptime(x, '%Y%m%d%H%M%S')
            channel = client.get_channel(config.Discord.DEV_TEST)
            await channel.send("KoL Cron Job successfully executed at: {}".format(date_time.strftime("%d/%m/%Y, %H:%M:%S")))
            os.remove(todelete)
        await asyncio.sleep(60)  # task runs every 60s


# Task - Use Cron to configure this properly. clean up duplicate method calls (RGB). Externalise URL.
async def daily_horse():
    await client.wait_until_ready()
    print("Daily Horse has started")
    while(True):
        channel = client.get_channel(config.Discord.DAILY_HORSE)
        red = random.SystemRandom().randint(1, 255)
        green = random.SystemRandom().randint(1, 255)
        blue = random.SystemRandom().randint(1, 255)
        embed = discord.Embed(colour=discord.Colour.from_rgb(red, green, blue))
        session = aiohttp.ClientSession()
        response = await session.get("https://api.giphy.com/v1/gifs/random?tag=horse&api_key={}".format(config.GIPHY_API_KEY))
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
        await ctx.send("Enjoy your daily horse GIF - {} brought to you by: {}".format(data['data']['title'], data['data']['username']))
        await ctx.send(embed=embed)
        await session.close()
        await asyncio.sleep(86400)  # runs every 24 hours

@client_command()
async def husky(ctx):
    red = random.SystemRandom().randint(1, 255)
    green = random.SystemRandom().randint(1, 255)
    blue = random.SystemRandom().randint(1, 255)
    embed = discord.Embed(colour=discord.Colour.from_rgb(red, green, blue))
    session = aiohttp.ClientSession()
    response = await session.get("https://api.giphy.com/v1/gifs/random?tag=husky&api_key={}".format(config.GIPHY_API_KEY))
    data = json.loads(await response.text())
    embed.set_image(url=data['data']['images']['original']['url'])
    await ctx.send("It's a husky! - {} brought to you by: {}".format(data['data']['title'], data['data']['username']))
    await ctx.send(embed=embed)
    await session.close()


client.loop.create_task(daily_horse())
client.loop.create_task(check_kol())
client.run(config.DISCORD_API_KEY)
