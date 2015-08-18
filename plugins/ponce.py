# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2015 Christophe-Marie Duquesne <chmd@chmd.fr>

"See PluginPonce"
from toflib import Plugin
import random

class PluginPonce(Plugin):
    "A plugin that asks the right questions"

    def handle_msg(self, msg_text, _chan, _nick):
        "When msg starts with 'elle', asks if it refers to the girfriend"

        words = msg_text.lower().strip().split(" ")

        if "elle" in words:
            if random.random() > .5:
                self.say("C'est ta meuf?")
