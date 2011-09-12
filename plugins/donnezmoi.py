import time

class PluginDonnezmoi:

    def __init__(self, bot):
        self.bot = bot

    def handle_msg(self, msg_text, chan):
        msg = msg_text.split(" ")
        if msg[0:2] == ['donnez', 'moi'] and msg[2] in ('un', 'une'):
            what = ' '.join(msg[3:])
            for m in what:
                self.bot.msg(self.bot.channels[0], m.upper())
                time.sleep(0.5)
