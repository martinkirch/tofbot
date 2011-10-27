# -*- coding: utf-8 -*-
from toflib import Plugin, InnocentHand

class PluginEuler(Plugin):

    def __init__(self, bot):
        Plugin.__init__(self, bot)
        balldata = [ "Essaye plus tard" , "Essaye encore" , "Pas d'avis"
                   , "C'est ton destin" , "Le sort en est jeté" , "Une chance sur deux"
                   , "Repose ta question" , "D'après moi oui" , "C'est certain"
                   , "Oui absolument" , "Tu peux compter dessus" , "Sans aucun doute"
                   , "Très probable" , "Oui" , "C'est bien parti"
                   , "C'est non" , "Peu probable" , "Faut pas rêver"
                   , "N'y compte pas" , "Impossible"
                   ]
        self.ball = InnocentHand(balldata)

    def handle_msg(self, msg_text, chan, nick):
        msg_text = msg_text.lower().strip()
        if msg_text.startswith("boule magique") and msg_text.endswith("?"):
            self.say(self.ball())
