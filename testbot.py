from bot import Tofbot

def print_resp(msg):
    print (" -> %s" % msg)

class TestTofbot(Tofbot):

    def __init__(self, nick, name, chan, origin):
        chans = [chan]
        Tofbot.__init__(self, nick, name, chans, debug=False)
        self.chan = chan
        self.origin = origin
        self.cb = print_resp

    def msg(self, chan, msg):
        if self.cb:
            self.cb(msg)
        else:
            print_resp(msg)

    def send(self, msg, cb=None):
        print ("<-  %s" % msg)
        saved_cb = self.cb
        self.cb = cb
        self.dispatch(self.origin, [msg, 'PRIVMSG', self.chan])
        self.cb = saved_cb
