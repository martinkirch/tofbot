from datetime import datetime
from toflib import cmd
import re

class TimeSlice():

    def __init__(self):
        t = datetime.now()
        self.date = t.date()
        self.hour = t.hour
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

    def __iadd__(self, other):
        self.count += other
        return self

class PluginLolrate:

    def __init__(self, bot):
        self.bot = bot
        self.lolRate = [TimeSlice()]
        self.bot._mutable_attributes['lolRateDepth'] = int

    def handle_msg(self, msg_text, chan, nick):
        lulz = len(re.findall("[Ll]+[oO]+[Ll]+", msg_text))
        if lulz > 0:
            ts = TimeSlice()
            if ts != self.lolRate[0]:
                self.lolRate.insert(0,ts)

            if len(self.lolRate) > self.bot.lolRateDepth:
                self.lolRate.pop()

            self.lolRate[0] += lulz

    @cmd(0)
    def cmd_lulz(self, chan, args):
        for lolade in self.lolRate:
            self.bot.msg(chan, str(lolade))
