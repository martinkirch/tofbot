#!/usr/bin/env python
"""
USAGE:

./bot.py nickname channel [other channels...]

Don't prepend a # to chan names
Tofbot will connect to freenode.net
"""

from irc import Bot
import sys

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
        
if __name__ == "__main__":
	if len(sys.argv) > 2:
		chans = map(lambda s: "#" + s, sys.argv[2:])
		b = Tofbot(sys.argv[1], 'Tofbot', chans)
		b.run('irc.freenode.net')
	else:
		print __doc__
