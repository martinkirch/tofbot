from irc import Bot

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

    def cmd_blague(self, chan):
        self.msg(chan, "Ceci est une blague")

    def cmd_chuck(self, chan):
        self.msg(chan, "Chuck Norris can solve the halting problem. He kicks the Turing machine's ass.")
