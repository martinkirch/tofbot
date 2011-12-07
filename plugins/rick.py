# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2011 Etienne Millon <etienne.millon@gmail.com>

from toflib import Plugin

class PluginRick(Plugin):

    def handle_msg(self, msg_text, chan, nick):
        rick_list = ["okqEVeNqBhc"
                    ,"XZ5TajZYW6Y"
                    ,"dQw4w9WgXcQ"
                    ]

        for r in rick_list:
            if r in msg_text:
                self.say("We're no strangers to love...")

