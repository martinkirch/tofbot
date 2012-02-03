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

# http://daringfireball.net/2010/07/improved_regex_for_matching_urls
# Public Domain
RE_URL = re.compile(
   r"""
    (?xi)
    \b
    (                           # Capture 1: entire matched URL
      (?:
        [a-z][\w-]+:                # URL protocol and colon
        (?:
          /{1,3}                        # 1-3 slashes
          |                             #   or
          [a-z0-9%]                     # Single letter or digit or '%'
                                        # (Trying not to match e.g. "URI::Escape")
        )
        |                           #   or
        www\d{0,3}[.]               # "www.", "www1.", "www2." … "www999."
        |                           #   or
        [a-z0-9.\-]+[.][a-z]{2,4}/  # looks like domain name followed by a slash
      )
      (?:                           # One or more:
        [^\s()<>]+                      # Run of non-space, non-()<>
        |                               #   or
        \(([^\s()<>]+|(\([^\s()<>]+\)))*\)  # balanced parens, up to 2 levels
      )+
      (?:                           # End with:
        \(([^\s()<>]+|(\([^\s()<>]+\)))*\)  # balanced parens, up to 2 levels
        |                                   #   or
        [^\s`!()\[\]{};:'".,<>?«»“”‘’]        # not a space or one of these punct chars
      )
    )
    """)

DOMAINS = [ "t.co/"
          ]

VIDEO_DOMAINS = [ "youtube"
                , "youtu.be"
                ]

def urls_in(text):
    return [m[0] for m in RE_URL.findall(text)]

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

    def expand_urls(self, urls):
        for url in urls:
            try:
                exp = urlExpand(url)
                self.say(exp)
            except:
                pass

    def display_titles(self, urls):
        for url in urls:
            try:
                t = getTitle(url)
                self.say(t)
            except:
                pass

    def handle_msg(self, msg_text, chan, nick):
        urls = urls_in(msg_text)
        murls = filter(is_mini, urls)
        vurls = filter(is_video, urls)
        self.expand_urls(murls)
        self.display_titles(vurls)
