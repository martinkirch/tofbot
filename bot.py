from irc import Bot

class Riddle(object):
    def __init__(self, riddle, answer, channel, writeback):
        self.riddle = riddle
        self.answer = answer
        self.channel = channel
        self.writeback = writeback
        self.remaining_msgs = 2
        self.writeback(self.riddle)

    def wait_answer(self, chan):
        if chan != self.channel:
            return False
        self.remaining_msgs -= 1
        if (self.remaining_msgs == 0):
            self.writeback(self.answer)
            return True
        return False

class Tofbot(Bot):

    def dispatch(self, origin, args):
        print ("o=%s a=%s" % (origin.sender, args))
        if (args[0] == 'End of /MOTD command.'):
            for chan in self.channels:
                self.write(('JOIN', chan))
        if origin.sender is None:
            return
        chan = args[2]
        msg = args[0]
        if (msg == '!blague'):
            self.cmd_blague(chan)
        if (msg == '!chuck'):
            self.cmd_chuck(chan)
        if (msg == '!devinette' and not self.active_riddle()):
            self.devinette = self.random_riddle(chan)
        if self.active_riddle():
            if (self.devinette.wait_answer(chan)):
                self.devinette = None

    def active_riddle(self):
        return (hasattr(self, 'devinette') and self.devinette is not None)

    def cmd_blague(self, chan):
        self.msg(chan, "Ceci est une blague")

    def cmd_chuck(self, chan):
        self.msg(chan, "Chuck Norris can solve the halting problem. He kicks the Turing machine's ass.")

    def random_riddle(self, chan):
        r = Riddle ("A ?", "B !", chan, lambda msg: self.msg(chan, msg))
        return r
