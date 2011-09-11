from toflib import cmd
import urllib2

class PluginEuler:

    def __init__(self, bot):
        self.bot = bot
        self._eulerScores = {}
        self._eulerNicks = set()

    def euler_update_data(self):
        for nick in self._eulerNicks:
            url = "http://projecteuler.net/profile/%s.txt" % nick
            s = urllib2.urlopen(url).read().split(',')
            if(len(s) >= 4):
                self._eulerScores[nick] = s[3]

    @cmd(0)
    def cmd_euler(self, chan, args):
        self.euler_update_data()
        for nick, score in self._eulerScores.items():
            self.bot.msg(chan, "%s : %s" %(nick, score))

    @cmd(1)
    def cmd_euler_add(self, chan, args):
        who = args[0]
        self._eulerNicks.add(who)

