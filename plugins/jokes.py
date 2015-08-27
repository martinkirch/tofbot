# -*- coding: utf-8 -*-
#
# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2011 Etienne Millon <etienne.millon@gmail.com>
#                    Martin Kirchgessner <martin.kirch@gmail.com>
#                    Nicolas Dumazet <nicdumz.commits@gmail.com>

from tofdata.chucknorris import chuckNorrisFacts
from tofdata.riddles import riddles
from tofdata.tofades import tofades
from tofdata.fortunes import fortunes
from tofdata.contrepeteries import contrepeteries
from toflib import cmd, InnocentHand, RiddleTeller, Plugin, CronEvent
import random
import time
from datetime import timedelta

class TofadeEvent(CronEvent):

    def __init__(self, plugin):
        CronEvent.__init__(self, plugin)
        self.period = timedelta(seconds=1)

    def fire(self):
        if (random.randint(0, 100) > self.plugin.bot.autoTofadeThreshold and
            (time.time() - self.plugin.lastTGtofbot) >= (self.plugin.bot.TGtime * 60)):
            self.plugin.say(self.plugin._tofades())

class PluginJokes(Plugin):

    def __init__ (self, bot):
        Plugin.__init__(self, bot)
        self._chuck = InnocentHand(chuckNorrisFacts)
        self._tofades = InnocentHand(tofades)
        self._riddles = InnocentHand(riddles)
        self._fortunes = InnocentHand(fortunes)
        self._contrepeteries = InnocentHand(contrepeteries)
        self.lastTGtofbot = 0
        bot._mutable_attributes["autoTofadeThreshold"] = int
        bot._mutable_attributes["riddleMaxDist"] = int
        ev = TofadeEvent(self)
        self.bot.cron.schedule(ev)

    @cmd(0)
    def cmd_fortune(self, chan, args):
        "Tell great philosophy"
        self.say(self._fortunes())

    @cmd(0)
    def cmd_chuck(self, chan, args):
        "Tell a Chuck Norris fact"
        self.say(self._chuck())

    @cmd(0)
    def cmd_tofade(self, chan, args):
        "Tof randomly"
        self.say(self._tofades())

    @cmd(0)
    def cmd_contrepeterie(self, chan, args):
        "Tell a contrepeterie"
        self.say(self._contrepeteries())

    @cmd(1)
    def cmd_tofme(self, chan, args):
        "Tof to someone (give a nickname)"
        who = args[0]
        self.say("%s : %s" % (who, self._tofades()))

    @cmd(0)
    def cmd_devinette(self, chan, args):
        "Riddle teller"
        if not self.active_riddle():
            self.devinette = self.random_riddle(chan)

    def on_join(self, chan, nick):
        if nick <> self.bot.nick:
            self.cmd_tofme(chan, [nick])

    def handle_msg(self, msg_text, chan, nick):
        stripped = msg_text.strip().lower()
        if stripped == "tg " + self.bot.nick:
            self.lastTGtofbot = time.time()
        elif stripped == "gg " + self.bot.nick:
            self.lastTGtofbot = 0
        elif stripped.find(self.bot.nick, 1) >= 0 and self.tofade_time():
            self.say(nick+": Ouais, c'est moi !")
        elif self.tofade_time(has_context=False):
            self.cmd_tofme(chan, [nick])
        if self.active_riddle():
            itsOver = self.devinette.wait_answer(chan, msg_text)
            if itsOver:
                self.devinette = None



    def active_riddle(self):
        return (hasattr(self, 'devinette') and self.devinette is not None)

    def random_riddle(self, chan):
        riddle = self._riddles()
        r = RiddleTeller (riddle,
                          chan,
                          self.say,
                          self.bot.riddleMaxDist)
        return r

    def on_kick(self, chan, reason):
        bot = self.bot
        if reason == bot.nick:
            respawn_msg = 'respawn, LOL'
        else:
            respawn_msg = 'comment ça, %s ?' % reason
        bot.msg(chan, respawn_msg)
