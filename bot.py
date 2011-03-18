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

random.seed()

class RiddleTeller(object):
    def __init__(self, riddle, channel, writeback):
        self.riddle, self.answer = riddle
        self.channel = channel
        self.writeback = writeback
        self.remaining_msgs = 4
        self.writeback(self.riddle)

    def wait_answer(self, chan, msg):
        if chan != self.channel:
            return False
        if msg == self.answer:
            self.writeback("10 points pour Griffondor.")
            return True
        self.remaining_msgs -= 1
        if self.remaining_msgs == 0:
            self.writeback(self.answer)
            return True
        return False

def attr_type(k):
    types = {"autoTofadeThreshold": 'int'}
    try:
        return types[k]
    except KeyError:
        return None

def in_whitelist(k):
    ty = attr_type(k)
    return (ty is not None)

def type_conv(value, ty):
    if ty == 'int':
        return int(value)
    assert False

class Tofbot(Bot):

    def __init__(self, nick, name, channels, password=None):
        Bot.__init__(self, nick, name, channels, password)
        self._jokes = Jokes()
        self._chuck = ChuckNorrisFacts()
        self._tofades = Tofades()
        self._riddles = Riddles()
        self._fortunes = Fortunes()
        self.joined = False
        self.autoTofadeThreshold = 95

    # those commands directly trigger cmd_* actions
    _simple_dispatch = set(('help', 'fortune', 'blague', 'chuck', 'tofade'))

    def dispatch(self, origin, args):
        print ("o=%s a=%s" % (origin.sender, args))

        commandType = args[1]

        if not self.joined:
            if (args[0] == 'End of /MOTD command.'):
                for chan in self.channels:
                    self.write(('JOIN', chan))
                self.joined = True
            return

        if commandType == 'PRIVMSG':
            msg_text = args[0]
            msg = msg_text.split(" ")
            cmd = msg[0]
            chan = args[2]

            assert cmd[0] == '!'
            cmd = cmd[1:]

            if chan == self.nick:
                chan = self.channels[0]

            if cmd in self._simple_dispatch:
                action = getattr(self, "cmd_" + cmd)
                action()
            elif (cmd == 'devinette' and not self.active_riddle()):
                self.devinette = self.random_riddle(chan)
            elif (cmd == 'get' and len(msg) == 2):
                key = msg[1]
                value = self.safe_getattr(key)
                if value is None:
                    self.msg(chan, "Ne touche pas à mes parties privées !")
                else:
                    self.msg(chan, "%s = %s" % (key, value))
            elif (cmd == 'set' and len(msg) == 3):
                key = msg[1]
                value = msg[2]
                ok = self.safe_setattr(key, value)
                if not ok:
                    self.msg(chan, "N'écris pas sur mes parties privées !")

            if self.active_riddle():
                if (self.devinette.wait_answer(chan, msg_text)):
                    self.devinette = None
            if self.joined:
                if random.randint(0, 100) > self.autoTofadeThreshold:
                    self.cmd_tofade(chan)
        elif commandType == 'JOIN':
            chan = args[0]
            self.cmd_tofade(chan)

    def safe_getattr(self, key):
        if not in_whitelist(key):
            return None
        if not hasattr(self, key):
            return "(None)"
        else:
            return str(getattr(self, key))

    def safe_setattr(self, key, value):
        try:
            ty = attr_type(key)
            if ty is None:
                return False
            else:
                value = type_conv (value, ty)
                setattr(self, key, value)
                return True
        except ValueError:
            pass

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

    def cmd_help(self, chan):
        self.msg(chan, "Commands should be entered in the channel or by private message")
        self.msg(chan, "Available commands : !blague !chuck !tofade !devinette !fortune !help")
        self.msg(chan, "you can also !get or !set autoTofadeThreshold")

    def random_riddle(self, chan):
        riddle = self._riddles.get()
        r = RiddleTeller (riddle, chan, lambda msg: self.msg(chan, msg))
        return r

if __name__ == "__main__":
	if len(sys.argv) > 2:
		chans = [ "#" + s for s in sys.argv[2:] ]
		b = Tofbot(sys.argv[1], 'Tofbot', chans)
		b.run('irc.freenode.net')
	else:
		print __doc__
