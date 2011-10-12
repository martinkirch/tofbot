from toflib import Plugin
import time

class PluginDonnezmoi(Plugin):

    def handle_msg(self, msg_text, chan, nick):
        msg = msg_text.split(" ")
        if msg[0:2] == ['donnez', 'moi'] and msg[2] in ('un', 'une'):
            what = ' '.join(msg[3:])
            for m in what:
                self.say(m.upper())
                time.sleep(0.5)
