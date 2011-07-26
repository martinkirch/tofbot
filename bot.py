#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
USAGE:

./bot.py nickname channel [other channels...]

Don't prepend a # to chan names
Tofbot will connect to freenode.net
"""

from datetime import datetime
from irc import Bot
from jokes import jokes
from chucknorris import chuckNorrisFacts
from riddles import riddles
from tofades import tofades
from fortunes import fortunes
from contrepetries import contrepetries
import time
import random
import sys
import re

random.seed()

def distance(string1, string2):
    """
    Levenshtein distance
    http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
    """
    string1 = ' ' + string1
    string2 = ' ' + string2
    dists = {}
    len1 = len(string1)
    len2 = len(string2)
    for i in range(len1):
        dists[i, 0] = i
    for j in range (len2):
        dists[0, j] = j
    for j in range(1, len2):
        for i in range(1, len1):
            if string1[i] == string2[j]:
                dists[i, j] = dists[i-1, j-1]
            else:
                dists[i, j] = min(dists[i-1, j] + 1,
                                  dists[i, j-1] + 1,
                                  dists[i-1, j-1] + 1
                                 )
    return dists[len1-1, len2-1]

def i_have(n, args):
    return n == len(args)

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
    

class RiddleTeller(object):
    """
    A gentleman (and a scholar) who likes to entertain its audience.
    """

    def __init__(self, riddle, channel, writeback, max_dist):
        self.riddle, self.answer = riddle
        self.channel = channel
        self.writeback = writeback
        self.remaining_msgs = 3
        self.writeback(self.riddle)
        self.max_dist = max_dist

    def wait_answer(self, chan, msg):
        """
        Called at each try.
        Returns True iff the riddle is over.
        """
        if chan != self.channel:
            return False
        if distance(msg.lower(), self.answer.lower()) < self.max_dist:
            self.writeback("10 points pour Griffondor.")
            return True
        self.remaining_msgs -= 1
        if self.remaining_msgs == 0:
            self.writeback(self.answer)
            return True
        return False

class InnocentHand(object):
    """
    A cute 6 years old girl, picking a random object
    from a given pool of candidates
    """
    def __init__(self, pool):
        """
        pool: list of candidates
        """
        self.pool = pool

    def __call__(self, index=None):
        if index:
            return self.pool[index % len(self.pool)]
        random.seed()
        return random.choice(self.pool)

class Tofbot(Bot):

    # Those attributes are published and can be changed by irc users
    # value is a str to object converter. It could do sanitization:
    # if value is incorrect, raise ValueError
    _mutable_attributes = {
        "autoTofadeThreshold": int ,
        "riddleMaxDist": int,
        "TGtime":int,
        "memoryDepth":int
    }

    def __init__(self, nick, name, channels, password=None, debug=True):
        Bot.__init__(self, nick, name, channels, password)
        self._jokes = InnocentHand(jokes)
        self._chuck = InnocentHand(chuckNorrisFacts)
        self._tofades = InnocentHand(tofades)
        self._riddles = InnocentHand(riddles)
        self._fortunes = InnocentHand(fortunes)
        self._contrepetries = InnocentHand(contrepetries)
        self.joined = False
        self.autoTofadeThreshold = 98
        self.riddleMaxDist = 2
        self.debug = debug
        self.TGtime = 5
        self.lastTGtofbot = 0
        self.pings = {}
        self.memoryDepth = 20
        self.lolRateDepth = 8
        self.msgMemory = []
        self.lolRate = [TimeSlice()]

    # those commands directly trigger cmd_* actions
    _simple_dispatch = set(('help'
                          , 'fortune'
                          , 'blague'
                          , 'chuck'
                          , 'tofade'
                          , 'tofme'
                          , 'devinette'
                          , 'get'
                          , 'set'
                          , 'ping'
                          , 'contrepetrie'
                          , 'lulz'
                          ))
    
    # line-feed-safe
    def msg(self, chan, msg):
        for m in msg.split("\n"):
            self.write(('PRIVMSG', chan), msg)
        
    def log(self, msg):
        if self.debug:
            print(msg)

    def try_join(self, args):
        if (args[0] in ['End of /MOTD command.',
                        "This server was created ... I don't know"]
                        ):
            for chan in self.channels:
                self.write(('JOIN', chan))
            self.joined = True


    def dispatch(self, origin, args):
        self.log("o=%s n=%s a=%s" % (origin.sender, origin.nick, args))
        
        senderNick = origin.nick
        commandType = args[1]

        if not self.joined:
            self.try_join(args)
            return

        if commandType == 'JOIN':
            chan = args[0]
            if senderNick == self.nick:
                self.cmd_tofade(chan, [])
            else:
                self.cmd_tofme(chan, [senderNick])
        
        elif commandType == 'PRIVMSG':
            msg_text = args[0]
            msg = msg_text.split(" ")
            cmd = msg[0]
            chan = args[2]
            
            self.pings[senderNick] = datetime.now()
            
            if msg_text.strip() == "TG " + self.nick:
                self.lastTGtofbot = time.time()

            if msg_text.strip() == "GG " + self.nick:
                self.lastTGtofbot = 0

            if (random.randint(0, 100) > self.autoTofadeThreshold and 
                (time.time() - self.lastTGtofbot) >= (self.TGtime * 60)):
                self.cmd_tofme(chan, [senderNick])
                
            if self.active_riddle():
                itsOver = self.devinette.wait_answer(chan, msg_text)
                if itsOver:
                    self.devinette = None

            if len(cmd) == 0:
                return
            
            lulz = len(re.findall("[Ll]+[oO]+[Ll]+", msg_text))
            if lulz > 0:
                ts = TimeSlice()
                if ts != self.lolRate[0]:
                    self.lolRate.insert(0,ts)
                    
                if len(self.lolRate) > self.lolRateDepth:
                    self.lolRate.pop()
                    
                self.lolRate[0] += lulz

            if chan == self.channels[0] and cmd[0] != '!':
                self.msgMemory.append("<" + senderNick + "> " + msg_text)
                if len(self.msgMemory) > self.memoryDepth:
                    del self.msgMemory[0]
            
            if cmd[0] != '!':
                return
            
            cmd = cmd[1:]

            if cmd in self._simple_dispatch:
                action = getattr(self, "cmd_" + cmd)
                action(self.channels[0], msg[1:])
            elif cmd == 'context':
                self.send_context(senderNick)

    def safe_getattr(self, key):
        if key not in self._mutable_attributes:
            return None
        if not hasattr(self, key):
            return "(None)"
        else:
            return str(getattr(self, key))

    def safe_setattr(self, key, value):
        try:
            converter = self._mutable_attributes.get(key)
            if converter is None:
                return False
            value = converter(value)
            setattr(self, key, value)
            return True
        except ValueError:
            pass

    def active_riddle(self):
        return (hasattr(self, 'devinette') and self.devinette is not None)
    
    def cmd_ping(self, chan, args):
        if i_have(1, args):
            who = args[0]
            if who in self.pings:
                self.msg(chan, 
                    "Last message from %s was on %s (btw my local time is %s)" % 
                    (who, self.pings[who].__str__(), datetime.now().__str__() ))
            else:
                self.msg(chan, "I havn't seen any message from " + who)

    def cmd_blague(self, chan, args):
        if i_have(0, args):
            self.msg(chan, self._jokes())

    def cmd_fortune(self, chan, args):
        if i_have(0, args):
            self.msg(chan, self._fortunes())

    def cmd_chuck(self, chan, args):
        if i_have(0, args):
            self.msg(chan, self._chuck())

    def cmd_tofade(self, chan, args):
        if i_have(0, args):
            self.msg(chan, self._tofades())
            
    def cmd_contrepetrie(self, chan, args):
        if i_have(0, args):
            self.msg(chan, self._contrepetries())

    def cmd_tofme(self, chan, args):
        if i_have(1, args):
            who = args[0]
            self.msg(chan, "%s : %s" % (who, self._tofades()))

    def cmd_devinette(self, chan, args):
        if i_have(0, args) and not self.active_riddle():
            self.devinette = self.random_riddle(chan)

    def cmd_lulz(self, chan, args):
        if i_have(0, args):
            for lolade in self.lolRate:
                self.msg(chan, str(lolade))

    def cmd_get(self, chan, args):
        if i_have(1, args):
            key = args[0]
            value = self.safe_getattr(key)
            if value is None:
                self.msg(chan, "Ne touche pas à mes parties privées !")
            else:
                self.msg(chan, "%s = %s" % (key, value))

    def cmd_set(self, chan, args):
        if i_have(2, args):
            key = args[0]
            value = args[1]
            ok = self.safe_setattr(key, value)
            if not ok:
                self.msg(chan, "N'écris pas sur mes parties privées !")

    def send_context(self, to):
        intro = "Last " + str(len(self.msgMemory)) + " messages sent on " + self.channels[0] + " :"
        self.msg(to, intro)
        
        for msg in self.msgMemory:
            self.msg(to, msg)

    def cmd_help(self, chan, args):
        if i_have(0, args):
            commands = ['!' + cmd for cmd in self._simple_dispatch]
            commands.append("!context")
            self.msg(chan, "Commands should be entered in the channel or by private message")
            self.msg(chan, "Available commands : " + ' '.join(commands))
            self.msg(chan, "you can also !get or !set " + ", ".join(self._mutable_attributes.keys()))
            self.msg(chan, "If random-tofades are boring you, enter 'TG " + self.nick + "' (but can be cancelled by GG " + self.nick + ")")

    def random_riddle(self, chan):
        riddle = self._riddles()
        r = RiddleTeller (riddle,
                          chan,
                          lambda msg: self.msg(chan, msg),
                          self.riddleMaxDist)
        return r

if __name__ == "__main__":
    if len(sys.argv) > 2:
        chans = [ "#" + s for s in sys.argv[2:] ]
        b = Tofbot(sys.argv[1], 'Tofbot', chans)
        b.run('irc.freenode.net')
    else:
        print __doc__
