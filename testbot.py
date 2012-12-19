# -*- coding: utf-8 -*-

from bot import Tofbot
import unittest
from collections import namedtuple
from httpretty import HTTPretty, httprettified
from plugins.euler import EulerEvent


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


def bot_action(bot, action):
    msgs = []

    def capture_out(msg):
        msgs.append(msg)

    bot.cb = capture_out
    action()
    return msgs


def bot_input(bot, msg):
    return bot_action(bot, lambda: bot.send(msg))


def bot_kick(bot, msg=None):
    return bot_action(bot, lambda: bot.kick(msg))


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
        l = bot_input(self.bot, inp)
        if isinstance(outp, str):
            outp = [outp]
        self.assertEqual(l, outp)

    def test_set_allowed(self):
        msg = "!set autoTofadeThreshold 9000"
        self.bot.send(msg)
        self._io("!get autoTofadeThreshold", "autoTofadeThreshold = 9000")

    def test_kick(self):
        l = bot_kick(self.bot)
        self.assertEqual(l, ["respawn, LOL"])

    def test_kick_reason(self):
        l = bot_kick(self.bot, "tais toi")
        self.assertEqual(l, ["comment ça, tais toi ?"])

    def test_dassin(self):
        self._io("tu sais", "je n'ai jamais été aussi heureux que ce matin-là")

    def test_donnezmoi(self):
        self._io("donnez moi un lol", ['L', 'O', 'L'])

    def test_eightball(self):
        l = bot_input(self.bot, "boule magique, est-ce que blabla ?")
        self.assertEquals(1, len(l))

    @httprettified
    def test_euler(self):
        euler_nick = 'leonhard'

        def set_score(score):
            url = "http://projecteuler.net/profile/%s.txt" % euler_nick
            country = 'country'
            language = 'language'
            level = 1
            text = "%s,%s,%s,Solved %d,%d" % (euler_nick,
                                              country,
                                              language,
                                              score,
                                              level,
                                              )
            HTTPretty.register_uri(HTTPretty.GET, url,
                                   body=text,
                                   content_type="text/plain")

        set_score(10)
        self.bot.send("!euler_add leonhard")

        # Get event to unschedule and manually fire it
        (event_k, event) = ((k, v) for (k, v)
                            in enumerate(self.bot.cron.events)
                            if isinstance(v, EulerEvent)).next()
        del self.bot.cron.events[event_k]

        self._io("!euler", "leonhard : Solved 10")
        set_score(15)
        l = bot_action(self.bot, event.fire)
        self.assertEqual(l, ["leonhard : Solved 10 -> Solved 15"])
