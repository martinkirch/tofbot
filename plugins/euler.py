# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2011 Etienne Millon <etienne.millon@gmail.com>
"See PluginEuler"
from toflib import cmd, Plugin, CronEvent, urlopen

class EulerEvent(CronEvent):
    "Every default period, poll projecteuler.net"

    def __init__(self, plugin):
        CronEvent.__init__(self, plugin)

    def fire(self):
        "If one of the scores has changed, print it"
        new_scores = self.plugin.fetch_scores()
        for nick, old_score in self.plugin.scores.items():
            try:
                new_score = new_scores[nick]
            except KeyError:
                continue
            if new_score != old_score:
                self.plugin.say("%s : %s -> %s" % (nick, old_score, new_score))
        self.plugin.scores = new_scores

class PluginEuler(Plugin):
    "A plugin to monitor projecteuler.net scores"

    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self.scores = {}
        self._euler_nicks = set()

    def fetch_scores(self):
        "Retrieve new scores from projecteuler.net for every nick"
        scores = {}
        try:
            for nick in self._euler_nicks:
                url = "http://projecteuler.net/profile/%s.txt" % nick
                data = urlopen(url).read().split(',')
                if(len(data) >= 4):
                    scores[nick] = data[3]
        except:
            pass
        return scores

    @cmd(0)
    def cmd_euler(self, _chan, _args):
        "Display PE scores"
        self.scores = self.fetch_scores()
        for nick, score in self.scores.items():
            self.say("%s : %s" %(nick, score))

    @cmd(1)
    def cmd_euler_add(self, _chan, args):
        "Add a PE account"
        who = args[0]
        self._euler_nicks.add(who)
        event = EulerEvent(self)
        self.bot.cron.schedule(event)

