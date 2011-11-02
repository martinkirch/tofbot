# -*- coding: utf-8 -*-
#
# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2011 Christophe-Marie Duquesne <chm.duquesne@gmail.com>
#                    Etienne Millon <etienne.millon@gmail.com>
from toflib import Plugin
from toflib import distance
from classifier import NaiveBayesClassifier, SqliteBackend

class PluginTeachMe(Plugin):

    def __init__(self, *args):
        Plugin.__init__(self, *args)
        self.classifier = NaiveBayesClassifier(SqliteBackend("db"))
        self.curr_msg = ''
        self.last_msg = ''
        self.last_joke = ()
        self.just_joked = False

    def get_what_to_learn(self):
        if self.curr_msg in ('CMB', 'cmb'):
            return 'CMB'
        if self.curr_msg in ('CTB', 'ctb'):
            return 'CTB'
        if self.curr_msg in ('TWSS', 'twss'):
            return "That's what she said!"
        return 'None'

    def got_congratulated(self):
        return self.curr_msg in ('GG', 'gg', 'GG Tofbot', 'gg Tofbot')

    def did_bad_joke(self):
        return self.curr_msg in ('TG', 'tg', 'TG Tofbot', 'tg Tofbot')

    def handle_msg(self, msg_text, chan, nick):
        just_joked = self.just_joked
        self.just_joked = False
        self.last_msg = self.curr_msg
        self.curr_msg = msg_text.strip()
        if self.got_congratulated():
            if self.last_joke:
                self.classifier.train(*self.last_joke)
        elif self.did_bad_joke():
            if self.last_joke:
                self.classifier.train(self.last_joke[0], 'None')
        else:
            scores = self.classifier.classify(self.curr_msg.split())
            joke = 'None'
            if scores:
                joke = scores[0][0]
            if joke != 'None':
                self.say(joke)
                self.last_joke = (self.curr_msg.split(), joke)
            else:
                if not just_joked:
                    self.classifier.train(self.last_msg.split(),
                            self.get_what_to_learn())
