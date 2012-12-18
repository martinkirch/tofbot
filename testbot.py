from bot import Tofbot
import unittest
from collections import namedtuple


def print_resp(msg):
    print (" -> %s" % msg)


class TestTofbot(Tofbot):

    def __init__(self, nick, name, chan, origin):
        chans = [chan]
        Tofbot.__init__(self, nick, name, chans, debug=False)
        self.chan = chan
        self.origin = origin
        self.cb = None
        self.joined = True

    def msg(self, chan, msg):
        if self.cb:
            self.cb(msg)
        else:
            print_resp(msg)

    def send(self, msg, cb=None):
        print ("<-  %s" % msg)
        self.dispatch(self.origin, [msg, 'PRIVMSG', self.chan])


class BotInput:

    def __init__(self, bot, msg):
        self.bot = bot
        self.msg = msg

    def __enter__(self):
        msgs = []

        def capture_out(msg):
            msgs.append(msg)

        self.bot.cb = capture_out
        self.bot.send(self.msg)
        return msgs[0]

    def __exit__(self, *args):
        pass


class TestCase(unittest.TestCase):

    def setUp(self):
        nick = "testbot"
        name = "Test Bot"
        chan = "#chan"
        Origin = namedtuple('Origin', ['sender', 'nick'])
        origin = Origin('sender', 'nick')
        self.bot = TestTofbot(nick, name, chan, origin)

    def test_set_allowed(self):
        msg = "!set autoTofadeThreshold 9000"
        self.bot.send(msg)

        with BotInput(self.bot, "!get autoTofadeThreshold") as l:
            self.assertEqual(l, "autoTofadeThreshold = 9000")
