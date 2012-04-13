# -*- coding: utf-8 -*-
#
# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2012 Etienne Millon <etienne.millon@gmail.com>

from BeautifulSoup import BeautifulSoup
import requests
import re

from toflib import Plugin

DOMAINS = [ "t.co/"
          , "tinyurl.com/"
          , "bit.ly/"
          ]

VIDEO_DOMAINS = [ "youtube"
                , "youtu.be"
                ]

def is_mini(url):
    for d in DOMAINS:
        if d in url:
            return True
    return False

def is_video(url):
    for d in VIDEO_DOMAINS:
        if d in url:
            return True
    return False

def urlExpand(url):
    r = requests.get(url)
    return r.url

def getTitle(url):
    r = requests.get(url)
    c = r.content
    s = BeautifulSoup(c)
    t = s.html.head.title.string
    return ''.join(t.split("\n")).strip()

class PluginExpand(Plugin):

    def on_url(self, url):
        if is_mini(url):
            try:
                exp = urlExpand(url)
                self.say(exp)
            except:
                pass

        if is_video(url):
            try:
                t = getTitle(url)
                self.say(t)
            except:
                pass
