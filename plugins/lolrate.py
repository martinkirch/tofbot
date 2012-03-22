# -*- coding: utf-8 -*-
#
# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2011 Etienne Millon <etienne.millon@gmail.com>
#                    Quentin Sabah <quentin.sabah@gmail.com>

"See PluginLolrate"
from datetime import datetime
from toflib import cmd, Plugin
import re

class TimeSlice():
    "An amount of time (1 hour) with an associated integer count"

    def __init__(self):
        now = datetime.now()
        self.date = now.date()
        self.hour = now.hour
        self.kevins = dict()
        self.count = 0

    def __str__(self):
        return "%s %02dh-%02dh : %d lolz" % ( self.date.strftime("%d %b")
                                            , self.hour
                                            , self.hour+1 % 24
                                            , self.count
                                            )
      

    def __cmp__(self, other):
        return cmp ( (self.date, self.hour)
                   , (other.date, other.hour)
                   )

    def __hash__(self):
        return hash(self.date) + hash(self.hour)

    def lol(self, nick, count):
        "Called when something funny happens on the chan"
        self.kevins.setdefault(nick, 0)
        self.kevins[nick] += count
        self.count += count

class PluginLolrate(Plugin):
    "A plugin to compute number of lols and the current Kevin of the day."

    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self.lol_rate = [TimeSlice()]
        bot._mutable_attributes['lolRateDepth'] = int

    def handle_msg(self, msg_text, _chan, nick):
        """
        If msg_text matches the lol regexp,
        increment the lolness for the current timeslice.
        """
        lol_regexp = "[lI1]+[o0u]+[lI1]+z?"
        lulz = len(re.findall(lol_regexp, msg_text, flags=re.IGNORECASE))
        if lulz > 0:
            current_ts = TimeSlice()
            if current_ts != self.lol_rate[0]:
                self.lol_rate.insert(0, current_ts)

            if len(self.lol_rate) > self.bot.lolRateDepth:
                self.lol_rate.pop()

            self.lol_rate[0].lol(nick, lulz)

    @cmd(0)
    def cmd_lulz(self, _chan, _args):
        "Display the number of lulz in the previous hours"
        for lolade in self.lol_rate:
            self.say(str(lolade))

    def compute_kevin(self):
        kevins = dict()
        for lolade in self.lol_rate:
            for kevin in lolade.kevins.iteritems():
                kevins.setdefault(kevin[0], 0)
                kevins[kevin[0]] += kevin[1]
        
        if len(kevins) > 0:
            def kevin_value(nick):
                "Fetch amount of lulz for a nick"
                return kevins.get(nick)
            kevin = max(kevins, key=kevin_value)
            lolades = kevins[kevin]
            return (kevin, lolades)
        else:
            return None

    @cmd(0)
    def cmd_kevin(self, _chan, _args):
        "Display the nick with the most lulz"
        k = self.compute_kevin()
        if k is None:
            self.say("pas de Kevin")
        else:
            kevin=k[0]
            lolades=k[1]
            plural = ""
            if lolades > 1:
                plural = "s"
            self.say("%s est le Kevin du moment avec %d lolade%s" %
                        (kevin, lolades, plural))

    def on_kick(self, chan, reason):
        k = self.compute_kevin()
        if k is not None:
            kevin=k[0]
            self.say("Au passage, %s est un sacré Kevin" % kevin)
