#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
USAGE:

./bot.py nickname channel [other channels...]

Don't prepend a # to chan names
Tofbot will connect to freenode.net
"""

from irc import Bot
from jokes import jokes
from chucknorris import chuckNorrisFacts
from riddles import riddles
from tofades import tofades
from fortunes import fortunes
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
        return random.choice(self.pool)

class Tofbot(Bot):

    # Those attributes are published and can be changed by irc users
    # value is a str to object converter. It could do sanitization:
    # if value is incorrect, raise ValueError
    _mutable_attributes = {
        "autoTofadeThreshold": int
    }

    def __init__(self, nick, name, channels, password=None):
        Bot.__init__(self, nick, name, channels, password)
        self._jokes = InnocentHand(jokes)
        self._chuck = InnocentHand(chuckNorrisFacts)
        self._tofades = InnocentHand(tofades)
        self._riddles = InnocentHand(riddles)
        self._fortunes = InnocentHand(fortunes)
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

    def cmd_blague(self, chan):
        self.msg(chan, self._jokes())

    def cmd_fortune(self, chan):
        self.msg(chan, self._fortunes())

    def cmd_chuck(self, chan):
        self.msg(chan, self._chuck())

    def cmd_tofade(self, chan):
        self.msg(chan, self._tofades())

    def cmd_help(self, chan):
        self.msg(chan, "Commands should be entered in the channel or by private message")
        self.msg(chan, "Available commands : !blague !chuck !tofade !devinette !fortune !help")
        self.msg(chan, "you can also !get or !set autoTofadeThreshold")

    def random_riddle(self, chan):
        riddle = self._riddles()
        r = RiddleTeller (riddle, chan, lambda msg: self.msg(chan, msg))
        return r

if __name__ == "__main__":
	if len(sys.argv) > 2:
		chans = [ "#" + s for s in sys.argv[2:] ]
		b = Tofbot(sys.argv[1], 'Tofbot', chans)
		b.run('irc.freenode.net')
	else:
		print __doc__
