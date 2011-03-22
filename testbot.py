from bot import Tofbot

class TestTofbot(Tofbot):

    def __init__(self, nick, name, chan, origin):
        chans = [chan]
        Tofbot.__init__(self, nick, name, chans, debug=False)
        self.chan = chan
        self.origin = origin

    def msg(self, chan, msg):
        print (" -> %s" % msg)

    def send(self, msg):
        print ("<-  %s" % msg)
        self.dispatch(self.origin, [msg, 'PRIVMSG', self.chan])
