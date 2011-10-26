from toflib import cmd, Plugin, CronEvent
import urllib2

class EulerEvent(CronEvent):

    def __init__(self, plugin):
        CronEvent.__init__(self, plugin)

    def fire(self):
        newScores = self.plugin.euler_update_data()
        for nick, oldScore in self.plugin._eulerScores.items():
            newScore = newScores[nick]
            if newScore != oldScore:
                self.plugin.say("%s : %s -> %s" % (nick, oldScore, newScore))
        self.plugin._eulerScores = newScores

class PluginEuler(Plugin):

    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self._eulerScores = {}
        self._eulerNicks = set()

    def euler_update_data(self):
        scores = {}
        for nick in self._eulerNicks:
            url = "http://projecteuler.net/profile/%s.txt" % nick
            s = urllib2.urlopen(url).read().split(',')
            if(len(s) >= 4):
                scores[nick] = s[3]
        return scores

    @cmd(0)
    def cmd_euler(self, chan, args):
        self._eulerScores = self.euler_update_data()
        for nick, score in self._eulerScores.items():
            self.say("%s : %s" %(nick, score))

    @cmd(1)
    def cmd_euler_add(self, chan, args):
        who = args[0]
        self._eulerNicks.add(who)
        ev = EulerEvent(self)
        self.bot.cron.schedule(ev)

