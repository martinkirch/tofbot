# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2011 Etienne Millon <etienne.millon@gmail.com>
#                    Christophe-Marie Duquesne <chm.duquesne@gmail.com>

"See PluginTwitter"
from toflib import cmd, Plugin, CronEvent
from bs4 import BeautifulSoup
import re
import requests
import json


def parse_tweet(url):
    r = requests.get(url)
    s = BeautifulSoup(r.text)
    container = s.find('div', {'class': 'permalink-tweet'})
    if container is None:
        return None
    tweet = container.find('p', {'class': 'js-tweet-text'})
    return tweet.get_text().strip()


class PluginTwitter(Plugin):
    """
    A twitter client plugin.
    It will expand tweets if a tweet URL is received.
    """

    def on_url(self, url):
        if re.match(r'https?://twitter.com/\w+/status/\d+', url):
            tweet = parse_tweet(url)
            if tweet:
                self.say(tweet)
