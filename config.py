#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import base64

# Version and changelog information
VERSION = "0.1.7"
CHANGELOG = """Version 0.1.7
        * Added !husky command to retrieve husky gifs from Giphy
        * Added !thanks command 
        * Removed !actions command as this is redundant due to !help

Version 0.1.6
        * Various code clean-up tasks
        * Renamed !commands to !help to stop overriding of Discord import 
        * Attempt to make code PEP8 compliant

Version 0.1.5
        * Resolved issues with bot changing channel

Version 0.1.4
        * Added ability to stream audio YouTube using !stream
        * Added mechanism to stream local mp3s

Version 0.1.3
        * Added daily horse gif retrieval from Giphy
        * Added H O R S E emojis whenever horse is mentioned in a sentence
        * Added random colour to embedded horse
        * Added port of God from TempleOS converted crudely from HolyC to Python

Version 0.1.2
        * Externalised token to environment variable
        * Updated uptime to be more human readable

Version 0.1.1
        * Resolved polling issue with cron job notifications

Version 0.1.0
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

Version 0.0.1       
        * First pass of info, flip, dazzyboo and serious commands
        * Integrated Twitch API poller"""

# List of COMMANDS
COMMANDS = """COMMANDS:
        * !flip - flip the bird to anyone that annoys you
        * !info <user> - retrieves the profile information for a user
        * !actions - provides a list of all available commands
        * !uptime - shows how long the bot has been up for
        * !dazzyboo - makes the bot have a mental breakdown
        * !serious - prints the serious plea to the current channel
        * !changelog - the changes since the last version
        * !music - plays music in the channel you're in
        * !stream <id> - streams audio from youtube to the voice channel
        * !husky - retrieves a random husky from giphy 
        * !commands - shows a list of enterable commands
"""

# YouTube Downloader
YTDL_FORMAT_OPTIONS = {
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

# FFmpeg configuration
FFMPEG_OPTIONS = {
    'options': '-vn'
}

# Environment variables
DISCORD_API_KEY = os.getenv('DISCORD_API_KEY', '')
GIPHY_API_KEY = os.getenv('GIPHY_API_KEY', '')

# God dictionary configuration
VOCABULARY = "vocab.dd"
with open(VOCABULARY) as vocabulary:
    GOD_DICTIONARY = dict(enumerate(vocabulary, 1))

# Discord channels


class Discord:
    DEV_TEST = 514244679907147776
    DAILY_HORSE = 791301208756584469


def base64_to_utf8(base64_message):
    base64_bytes = base64_message.encode('utf-8')
    return base64.b64decode(base64_bytes).decode('utf-8')


# URLs
GIPHY_API = 'https://api.giphy.com/v1/gifs/random?tag={}&api_key={}'
GIPHY_API_HORSE_REQUEST = GIPHY_API.format("horse", GIPHY_API_KEY)
GIPHY_API_HUSKY_REQUEST = GIPHY_API.format("husky", GIPHY_API_KEY)


# Static text fields
ON_READY = "No adventure is complete without Jingle hat and Jingle feet"
DAZZY_RANT = base64_to_utf8("SGVsbG8gZm9sa3MuIFNvcnJ5IGZvciB0aGUgdHlwb3MgbGFkcy4gV2hhdCBhbiBldmVudGZ1bCBmdWNraW5nIG5pZ2h0IHRoYXQgd2FzIG9uIERpc2NvcmQsIHRoZW4gd2FrZXMgdXAgdG8gYXcgdGhhdCB0aGlzIG1vcm5pbmcuIEFueXdheSwgU3RhdGVtZW50LiBGb3IgdGhlIGxhc3QgMiBtb250aHMgbWUgbiBDYWl0bGluIGhhdmUgYmVlbiBjaGF0dGluZyBhIGxvdCBhcyB5ZSdzIGtub3cuIEFuZCB3ZSd2ZSBldmVuIG1ldCB1cCBhIGZldyB0aW1lcy4gQXMgc29tZSBvZiB5b3VzIGtub3csIEkgbGlrZWQgaGVyIGEgbG90IGNhbiB5ZSBiZWxpZXZlIGl0PyBJJ2QgZXZlbiBnbyBhcyBmYXIgYXMgc2F5aW5nIHdlIHdlcmUgc2VlaW5nIGVhY2ggb3RoZXIuIEF0IG9uZSBwb2ludCB3ZSBib3RoIGFja25vd2xlZGdlZCB3ZSBib3RoIHdhbnRlZCB0byBiZSBhIGNvdXBsZS4gQW55d2F5LCB0aGlzIGxhc3Qgd2VlayBvciBzbyBoYXMgYmVlbiBhIGZ1Y2tpbiBtaW5kIGdhbWUgdG8gaGVyLiBJIG1hZGUgYSBkYWZ0IGRlY2lzaW9uIGF0IHRoZSBzdGFydCBvZiB3aGF0ZXZlciBpdCB3YXMgd2UndmUgYmVlbiBkb2luZy4gSSB0b2xkIGhlciBJIHdhc25hZSBpbnZvbHZlZCBpbiBzb21ldGhpbmcgdGhhdCBJIHdhcyBhbmQgSSd2ZSBiZWVuIGdldHRpbmcgcHVuaXNoZWQgYSBmdWNrZXIuIFNoZSdzIGJlZW4gdXNpbmcgU3RlcGhlbiB0byBnZXQgYmFjayBhdCBtZS4gWW91IHNlZSwgdGhlcmUncyBiZWVuIHBhdHRlciBpbiBoZXJlIGFib3V0IGhlciBnb2luZyBvbiBhIGRhdGUgd2kgU3RlcGhlbiBhbmQgaXQgbWFkZSBtZSBhIHdlZSBiaXQgaW5zZWN1cmUuIEl0IGhhcHBlbnMuIFNvIGFzIHB1bmlzaG1lbnQgc2hlJ3MgYmVlbiBwbGF5aW5nIHdpIGhpbSBhbmQgY2hhdHRpbmcgd2kgaGltIGFuZCBjb21wbGV0ZWx5IGlnbm9yaW5nIG1lLiBUaGVuIHdoZW4gSSBhc2sgd2hhdHMgZ29pbmcgb24sIHNoZSBzYXlzIG5vdGhpbmcgYW5kIG5vdCB0byB3b3JyeSBhbmQgdGhhdCB3ZSdsbCBiZSBmaW5lIGFuZCB0aGUgc2hlJ3MgcmlnaHQgYmFjayBvbiB3aSBoaW0uIFRoaXMgaGFzIGNhdXNlIHRoZSBsYXN0IHdlZWsgb3Igc28gb2YgYW54aWV0eSBhdHRhY2tzIGFuZCBtZW50YWwgZnVja2luIGJyZWFrZG93bnMuIDMgdGltZXMgSSd2ZSB0cmllZCB0byB3YWxrIGF3YXkgZnJvbSBoZXIgYW5kIDMgdGltZXMgc2hlJ3MgcGhvbmVkIG1lLiBPbmNlIHRvIHRlbGwgbWUgSSdtIGFuIGlkaW90IGFuZCBJJ20gb3ZlciB0aGlua2luZyB0aGluZ3MuIE9uY2UgdG8gdGVsbCBtZSB0byBzdG9wIHBsYXlpbmcgZ2FtZXMgd2l0aCBmb2xrIHdpdGhvdXQgaGVyIChlc3BlY2lhbGx5IGJ1dHRlcnMpIGFuZCBvbmNlIGJlY2F1c2Ugb25lIG9mIHRoZXNlIGN1bnRzIHRvbGQgaGVyLiBJIHRvbGQgdGhlbSBhYm91dCB1cy4gSSdtIG5vIG1hZCB0aG91Z2guIFdoYXQgSSBhbSBtYWQgYWJvdXQgaXMgdGhlIHBob25lIGNhbGwgSSBnb3QgbGFzdCBuaWdodCBmcm9tIGhlci4gV2hlcmUgc2hlIHRvbGQgbWUgdGhhdCBJIHdhc24ndCB0byBzcGVhayB0byBhbnlvbmUgaW4gdGhlIGRpc2NvcmQuIFNoZSB0b2xkIG1lIHRoYXQsIGZvciBteSBvd24gd2VsbCBiZWluZyBJIG5lZWRlZCBhIGJyZWFrIGFuZCBmb3IgdGhhdCByZWFzb24gSSB3YXNuJ3QgdG8gcmVhY2ggb3V0IHRvIGFueW9uZSBhbmQgaWYgSSBkaWQsIHNoZSdkIGZpbmQgb3V0LiBJZiBJIHBsYXllZCBnYW1lcyB3aXRoIGFueW9uZSBzaGUnZCBmaW5kIG91dC4gSWYgSSBhcHBlYXJlZCBvZmZsaW5lIHdpdGggc29tZW9uZSwgc2hlJ2QgZmluZCBvdXQuIE1lYW53aGlsZSB0ZWxsaW5nIG1lIGl0J3MgY2F1c2UgZXZlcnlvbmUgY2FyZXMuIEkgY291bGRuYWUgcmVhbGx5IHdvcmsgb3V0IHdoYXQgd2FzIGhhcHBlbmluZy4=")
DAZZY_RANT_2 = base64_to_utf8("U28gbmF0dXJhbGx5IEkganVtcCB1cCBhbmQgSSdtIG9uIHRoZSBkaXNjb3JkIHRvIGJ1dHRlcnMuIElnbm9yZWQuIFRoZW4gYSB0ZXh0IGNvbWVzIGluIGZyb20gaGVyIGFza2luZyB3aHkgaW0gbWVzc2FnaW5nIGhpbS4gVGhlbiBoZSBtZXNzYWdlcyBtZS4gVHVybnMgb3V0IGZvbGsgYXJlbid0IGlnbm9yaW5nIG1lIGNhdXNlIHRoZXkgY2FyZSBpdCdzIGJlY2F1c2Ugc2hlJ3MgdG9sZCBzb21lIGN1bnRzLCBJIGRvbid0IGtub3cgZXZlcnlvbmUsIHRoYXQgSSd2ZSBtYWRlIGFsbCB0aGlzIHNoaXRlIHVwLiBJIGRvbid0IGtub3cgaG93IHNoZSdzIG1hZGUgaXQgbG9vayBlaXRoZXIuIElmIHNoZSdzIG1hZGUgbWUgbG9vayBwYXRoZXRpYyBhbmQgbG9uZWx5IG9yIGlmIEkgbG9vayBsaWtlIGEgcHN5Y2hvIGJ1dCBJIGNhbiBhYnNvbHV0ZWx5IGFzc3VyZSB5b3VzIHNoZSdzIG1hbmlwdWxhdGluZyB0aGUgZnVja2luIGxvdCBvZiB1cyBhbmQgc2hlJ3MgbG92aW5nIGl0LiBJIGtub3cgbW9zdCBvZiB5b3VzIHByb2JhYmx5IGRvbid0IGNhcmUgYnV0IHRoaXMgaXMgd2hhdCdzIGhhcHBlbmluZyBiZWhpbmQgdGhlIHNjZW5lcy4gMiBmb2xrIEkgY29uc2lkZXIgbWF0ZXMgYW5kIGhhdmUga25vd24gZm9yIHllYXIsIGFsYmVpdCBJJ3ZlIG5ldmVyIG1ldCBidXR0ZXJzIGJ1dCBzdGlsbCwgaGF2ZSBiZWVuIHR1cm5lZCBhZ2FpbnN0IG1lIGNhdXNlIHRoZXkndmUgYmVlbiBjb252aW5jZWQgaW0gbHlpbmcgYWJvdXQgc29tZXRoaW5nLiBIYXZlIGEgbmljZSBkYXksIEkgZG9uJ3QgZXhwZWN0IGFueWN1bnQgdG8gdGFrZSBzaWRlcywgaW0gbm8gYSB3ZWFuIGJ1dCBpdCdkIGJlIG5pY2UgdG8gaGF2ZSBtb3JlIGZvbGsgaW4gdGhlIGtub3cgaW5zdGVhZCBvZiBoZXIgcHJldGVuZGluZyBpbiB0aGF0IGRpc2NvcmQgdGhhdCBldmVyeXRoaW5ncyBmaW5lIGFuZCBpbSBvdXRzaWRlIGZlZWxpbmcgbGlrZSBzaGl0ZSBjYXVzZSB3aWxreSdzIHRoZSBvbmx5IGN1bnQgdGhhdCB3YW50cyB0byB0YWxrIHRvIG1lLiBTaGUgbWlnaHQgZmxpcCB0aGlzLCB0ZWxsIHlvdXMgaW0gYXQgaXQgYW5kIGltIG1ha2luZyBzaGl0ZSB1cCBhZ2Fpbi4gQW5kIHlvdXMgbWlnaHQgYmVsaWV2ZSBoZXIgY2F1c2Ugc2hlJ3MgYSBsYXNzaWUgYnV0IEkgY2FuIGFzc3VyZSB5b3VzLCBzaGUncyBhIGJldHRlciBsaWFyIHRoYW4gSSBhbSBhbmQgSSBjb3VsZG5hZSBtYWtlIHNvbWV0aGluZyB0aGlzIGZ1Y2tpbiBjaGlsZGlzaCBhbmQgcGV0dHkgdXAgaWYgSSB0cmllZC4gSG9wZSB0byBzZWUgYWxsIG15IGdhbWluZyBwYWxzIG9uIFJhaW5ib3cgNiBub3cgdGhhdCBJJ20gZnJlZSBhbmQgYWxsb3dlZCB0byBwbGF5IGdhbWVzIG15c2VsZiBhZ2Fpbi4gR29kIGJsZXNzLg==")
SERIOUS_RANT = base64_to_utf8("SGVsbG8gZm9sa3MuIFRoaXMgaXMgYSBzZXJpb3VzIHBvc3Qgc28gaSdtIGFza2luZyB5b3UgdG8gcGxlYXNlIHJlYWQgaXQuIFNvbWUgb2YgeW91cyB3aWxsbmFlIGtub3cgYnV0IGkgd2FzIHNlZWluZyBzb21lb25lIGZvciBhIHdlZSB3aGlsZSB0aGVyZS4gU2hlIHR1cm5lZCBvdXQgdG8gYmUgYSBwc3ljaG8gaW4gdGhlIGVuZCwgc29tZSBmb2xrIGtub3cgdGhlIGRldGFpbHMgb3RoZXJzIGRpbm5hZSBuZWVkIHRvLiBXZWxsIGluIHRoZSBsYXN0IGZldyBkYXlzIGkndmUgc3RhcnRlZCBnZXR0aW5nIGRlYXRoIHRocmVhdHMgZnJvbSByYW5kb20gY3VudHMuIEknbGwgbm8gZ28gaW50byB0b28gbXVjaCBkZXRhaWwsIGJ1dCB0aGUgd2VlIGNvdyBoYXMgYmVlbiB0ZWxsaW5nIGZvbGsgb25saW5lIHNvbWV3aGVyZSB0aGF0IGknbSBhIHBhZWRvLiBJIGRpbm5hZSBrbm93IHdoZXJlLCBpIGRpbm5hZSBrbm93IGhvdyBtYW55IGZvbGssIGkgbm8gbm90aGluZy4gSW0gd2FudGluZyBmb2xrIHRvIGtub3cgdGhpcyBjYXVzZSBpZiBhbnlvbmUgZ2V0cyBhIG1lc3NhZ2UsIGl0J3MgdW5saWtlbHkgYnV0IGlmIHlvdSBkbywgcGxlYXNlIHRlbGwgbWUsIHNjcmVlbnNob3QgaXQsIHJlcG9ydCBpdCBhbmQgdGhlbiBibG9jayB0aGVtLiBJJ20gdGFraW5nIGFueSBuZXcgaW5mb3JtYXRpb24gaSBnZXQgdG8gdGhlIHBvbGljZS4gVGhhbmtzIGZvciByZWFkaW5nLiBHb2QgYmxlc3M=")

# Templates
USER_INFO = """User Information:
            
            * Name: {}, 
            * ID: {} 
            * Discriminator: {}, 
            * Created at: {}, 
            * Avatar {}"""

# Emojis

class Emoji:
    MIDDLE_FINGER = '🖕'
    REGIONAL_INDICATOR_H = '🇭'
    REGIONAL_INDICATOR_O = '🇴'
    REGIONAL_INDICATOR_R = '🇷'
    REGIONAL_INDICATOR_S = '🇸'
    REGIONAL_INDICATOR_E = '🇪'

HORSE_EMOJI_LIST = [Emoji.REGIONAL_INDICATOR_H,
Emoji.REGIONAL_INDICATOR_O,
Emoji.REGIONAL_INDICATOR_R,
Emoji.REGIONAL_INDICATOR_S,
Emoji.REGIONAL_INDICATOR_E]

