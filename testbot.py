# -*- coding: utf-8 -*-

from bot import Tofbot
import unittest
from collections import namedtuple


def print_resp(msg):
    print (" -> %s" % msg)


class TestTofbot(Tofbot):

    def __init__(self, nick, name, chan, origin):
        chans = [chan]
        self.nick = nick
        Tofbot.__init__(self, nick, name, chans, debug=False)
        self.chan = chan
        self.origin = origin
        self.cb = None

    def msg(self, chan, msg):
        if self.cb:
            self.cb(msg)
        else:
            print_resp(msg)

    def send(self, msg):
        print ("<-  %s" % msg)
        self.dispatch(self.origin, [msg, 'PRIVMSG', self.chan])

    def kick(self, msg=None):
        if msg is None:
            msg = self.nick
        self.dispatch(self.origin, [msg, 'KICK', self.chan, self.nick])


class BotAction:
    def __init__(self, bot, action):
        """
        If length=None, just expect one and return it (not a list).
        """
        self.bot = bot
        self.action = action
        self.msgs = []

    def __enter__(self):
        def capture_out(msg):
            self.msgs.append(msg)

        self.bot.cb = capture_out
        self.action()
        return self.msgs

    def __exit__(self, *args):
        pass


def bot_input(bot, msg):
    return BotAction(bot, lambda: bot.send(msg))


def bot_kick(bot, msg=None):
    return BotAction(bot, lambda: bot.kick(msg))


class TestCase(unittest.TestCase):

    def setUp(self):
        nick = "testbot"
        name = "Test Bot"
        chan = "#chan"
        Origin = namedtuple('Origin', ['sender', 'nick'])
        origin = Origin('sender', 'nick')
        self.bot = TestTofbot(nick, name, chan, origin)
        cmds = ['!set autoTofadeThreshold 100']
        for cmd in cmds:
            self.bot.dispatch(origin, [cmd, 'BOTCONFIG', 'PRIVMSG', '#config'])

        self.bot.joined = True

    def _io(self, inp, outp):
        """
        Test that a given input produces a given output.
        """
        with bot_input(self.bot, inp) as l:
            if isinstance(outp, str):
                outp = [outp]
            self.assertEqual(l, outp)

    def test_set_allowed(self):
        msg = "!set autoTofadeThreshold 9000"
        self.bot.send(msg)
        self._io("!get autoTofadeThreshold", "autoTofadeThreshold = 9000")

    def test_kick(self):
        with bot_kick(self.bot) as l:
            self.assertEqual(l, ["respawn, LOL"])

    def test_kick_reason(self):
        with bot_kick(self.bot, "tais toi") as l:
            self.assertEqual(l, ["comment ça, tais toi ?"])

    def test_dassin(self):
        self._io("tu sais", "je n'ai jamais été aussi heureux que ce matin-là")

    def test_donnezmoi(self):
        self._io("donnez moi un lol", ['L', 'O', 'L'])
