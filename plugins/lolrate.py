from datetime import datetime
from toflib import cmd, Plugin
import re

class TimeSlice():

    def __init__(self):
        t = datetime.now()
        self.date = t.date()
        self.hour = t.hour
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
      self.kevins.setdefault(nick,0)
      self.kevins[nick] += count
      self.count += count

class PluginLolrate(Plugin):

    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self.lolRate = [TimeSlice()]
        bot._mutable_attributes['lolRateDepth'] = int

    def handle_msg(self, msg_text, chan, nick):
        lulz = len(re.findall("[Ll]+[oO]+[Ll]+", msg_text))
        if lulz > 0:
            ts = TimeSlice()
            if ts != self.lolRate[0]:
                self.lolRate.insert(0,ts)

            if len(self.lolRate) > self.bot.lolRateDepth:
                self.lolRate.pop()

            self.lolRate[0].lol(nick,lulz)

    @cmd(0)
    def cmd_lulz(self, chan, args):
        for lolade in self.lolRate:
            self.say(str(lolade))

    @cmd(0)
    def cmd_kevin(self, chan, args):
        kevins = dict()
        for lolade in self.lolRate:
            for kevin in lolade.kevins.iteritems():
                kevins.setdefault(kevin[0],0)
                kevins[kevin[0]] += kevin[1]
        
        if len(kevins) > 0:
            kevin = max(kevins,key=lambda a: kevins.get(a))
            lolades = kevins[kevin]
            self.say(str(kevin) + " est le Kevin du moment avec " + str(lolades) + " lolade" + ("s" if lolades > 1 else ""))
        else:
            self.say("pas de Kevin")

