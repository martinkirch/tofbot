# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2011 Etienne Millon <etienne.millon@gmail.com>

"See PluginDonnezmoi"
from toflib import Plugin
import time

class PluginDonnezmoi(Plugin):
    "A 'gimme a xxx' banner generator plugin"

    def handle_msg(self, msg_text, _chan, _nick):
        "Write a banner if input looks like a banner query"
        msg = msg_text.split(" ")
        if msg[0:2] == ['donnez', 'moi'] and msg[2] in ('un', 'une'):
            what = ' '.join(msg[3:])
            for char in what:
                self.say(char.upper())
                time.sleep(0.5)
