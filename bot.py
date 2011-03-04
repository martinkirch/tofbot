from irc import Bot

class Tofbot(Bot):
    def dispatch(self, origin, args):
        print ("o=%s a=%s" % (str(origin.sender), args))
        if (args[0] == 'End of /MOTD command.'):
            for chan in self.channels:
                self.write(('JOIN', chan))
