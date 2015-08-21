# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2015 Christophe-Marie Duquesne <chmd@chmd.fr>

"See PluginLag"
from toflib import Plugin
import datetime

class PluginLag(Plugin):
    "Lag: time between a mention and the answer"

    def __init__(self):
        self.watched = [] # list of nicks
        self.last_mention = {} # tuples (datetime, nick, message)
        self.threshold = datetime.timedelta(seconds=20*60) # lag threshold


    def handle_msg(self, msg_text, _chan, me):
        "If the lag exceeds the threshold and we feel like it, report it"

        now = datetime.datetime.now()

        if not me in self.watched:
            self.watched.append(me)

        words = msg_text
                    .replace(":", " ")
                    .replace(",", " ")
                    .strip()
                    .split(" ")

        # did I mention anybody?
        for nick in self.watched:
            if nick in words and nick != me:
                self.last_mention[nick] = (now, me, msg_text)

        # is there a pending mention for me?
        mention = self.last_mention.get(me, None)
        if mention is not None:
            timestamp, nick, msg = mention
            lag = now - timestamp
            if lag > self.threshold and self.tofade_time():
                self.say(
                    "Le %s-lag du moment est %s (pour <%s>: %s)." %
                    (me, str(lag), nick, msg)
                    )

            # wipe out the pending mention
            self.last_mention[me] = None
