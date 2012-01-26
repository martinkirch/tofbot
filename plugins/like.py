# -*- coding: utf-8 -*-
#
# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2012 Etienne Millon <etienne.millon@gmail.com>

from collections import deque
from toflib import cmd, Plugin

class PluginLike(Plugin):

    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self.history = deque([], 2)
        self.scores = {}

    def handle_msg(self, msg_text, chan, nick):
        self.history.append(nick)

    @cmd(0)
    def cmd_like(self, _chan, _args):
        h = self.history
        if len(h) == 2:
            n = h[0]
            if n not in self.scores:
                self.scores[n] = 0
            self.scores[n] += 1

    @cmd(1)
    def cmd_score(self, _chan, args):
        n = args[0]
        if n not in self.scores:
            self.say("%s n'est pas très populaire." % n)
        else:
            s = self.scores[n]
            self.say("%d" % s)
