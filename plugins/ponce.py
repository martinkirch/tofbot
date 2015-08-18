# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2015 Christophe-Marie Duquesne <chmd@chmd.fr>

"See PluginPonce"
from toflib import Plugin
import time

class PluginPonce(Plugin):
    "A plugin that asks the right questions"

    def handle_msg(self, msg_text, _chan, _nick):
        "When msg starts with 'elle', asks if it refers to the girfriend"

        msg = msg_text.strip().lower()
        first_word = msg[:msg.find(" ")]
        if first_word == "elle":
            self.say("C'est ta meuf?")
