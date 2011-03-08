#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
USAGE:

./bot.py nickname channel [other channels...]

Don't prepend a # to chan names
Tofbot will connect to freenode.net
"""

from irc import Bot
from jokes import Jokes
from chucknorris import ChuckNorrisFacts
from riddles import Riddles
from tofades import Tofades
from fortunes import Fortunes
import random
import sys

class Riddle(object):
    def __init__(self, riddle, answer, channel, writeback):
        self.riddle = riddle
        self.answer = answer
        self.channel = channel
        self.writeback = writeback
        self.remaining_msgs = 4
        self.writeback(self.riddle)

    def wait_answer(self, chan):
        if chan != self.channel:
            return False
        self.remaining_msgs -= 1
        if (self.remaining_msgs == 0):
            self.writeback(self.answer)
            return True
        return False

def in_whitelist(k):
    return k in []

class Tofbot(Bot):

    def __init__(self, nick, name, channels, password=None):
        Bot.__init__(self, nick, name, channels, password)
        self._jokes = Jokes()
        self._chuck = ChuckNorrisFacts()
        self._tofades = Tofades()
        self._riddles = Riddles()
        self._fortunes = Fortunes()
        self.joined = False

    def dispatch(self, origin, args):
        print ("o=%s a=%s" % (origin.sender, args))
        if (args[0] == 'End of /MOTD command.'):
            for chan in self.channels:
                self.write(('JOIN', chan))
                self.cmd_tofade(chan)
            self.joined = True
        if origin.sender is None:
            return
        chan = args[2]
        msg = args[0].split(" ")
        cmd = msg[0]
        if (cmd == '!help'):
            self.msg(chan, "Commandes : !blague !chuck !tofade !devinette !fortune !help")
        if (cmd == '!fortune'):
            self.cmd_fortune(chan)
        if (cmd == '!blague'):
            self.cmd_blague(chan)
        if (cmd == '!chuck'):
            self.cmd_chuck(chan)
        if (cmd == '!tofade'):
            self.cmd_tofade(chan)
        if (cmd == '!devinette' and not self.active_riddle()):
            self.devinette = self.random_riddle(chan)
        if (cmd == '!get' and len(msg) == 2):
            key = msg[1]
            value = self.safe_getattr(key)
            if value is None:
                self.msg(chan, "Ne touche pas à mes parties privées !")
            else:
                self.msg(chan, "%s = %s" % (key, value))
        if (cmd == '!set' and len(msg) == 3):
            key = msg[1]
            value = msg[2]
            ok = self.safe_setattr(key, value)
            if not ok:
                self.msg(chan, "N'écris pas sur mes parties privées !")
        if self.active_riddle():
            if (self.devinette.wait_answer(chan)):
                self.devinette = None
        if self.joined:
            random.seed()
            if random.randint(0, 100) > 98:
                self.cmd_tofade(chan)

    def safe_getattr(self, key):
        if not in_whitelist(key):
            return None
        if not hasattr(self, key):
            return "(None)"
        else:
            return str(getattr(self, key))

    def safe_setattr(self, key, value):
        if not in_whitelist(key):
            return False
        else:
            setattr(self, key, value)
            return True

    def active_riddle(self):
        return (hasattr(self, 'devinette') and self.devinette is not None)

    def cmd_blague(self, chan):
        self.msg(chan, self._jokes.get())

    def cmd_fortune(self, chan):
        self.msg(chan, self._fortunes.get())

    def cmd_chuck(self, chan):
        self.msg(chan, self._chuck.get())
    
    def cmd_tofade(self, chan):
        self.msg(chan, self._tofades.get())

    def random_riddle(self, chan):
        text = self._riddles.get()
        r = Riddle (text[0], text[1], chan, lambda msg: self.msg(chan, msg))
        return r
        
if __name__ == "__main__":
	if len(sys.argv) > 2:
		chans = [ "#" + s for s in sys.argv[2:] ]
		b = Tofbot(sys.argv[1], 'Tofbot', chans)
		b.run('irc.freenode.net')
	else:
		print __doc__
