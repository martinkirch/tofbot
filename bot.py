#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
USAGE:

./bot.py nickname channel [other channels...]

Don't prepend a # to chan names
Tofbot will connect to freenode.net
"""

from datetime import datetime
from irc import Bot
from jokes import jokes
from chucknorris import chuckNorrisFacts
from riddles import riddles
from tofades import tofades
from fortunes import fortunes
from contrepetries import contrepetries
import time
import random
import sys
import os
import plugins
import types
from toflib import cmd, _simple_dispatch, distance, InnocentHand, RiddleTeller

import plugins.euler
import plugins.lolrate
import plugins.donnezmoi

random.seed()

class Tofbot(Bot):

    # Those attributes are published and can be changed by irc users
    # value is a str to object converter. It could do sanitization:
    # if value is incorrect, raise ValueError
    _mutable_attributes = {
        "autoTofadeThreshold": int ,
        "riddleMaxDist": int,
        "TGtime":int,
        "memoryDepth":int
    }

    def __init__(self, nick, name, channels, password=None, debug=True):
        Bot.__init__(self, nick, name, channels, password)
        self._jokes = InnocentHand(jokes)
        self._chuck = InnocentHand(chuckNorrisFacts)
        self._tofades = InnocentHand(tofades)
        self._riddles = InnocentHand(riddles)
        self._fortunes = InnocentHand(fortunes)
        self._contrepetries = InnocentHand(contrepetries)
        self.joined = False
        self.autoTofadeThreshold = 98
        self.riddleMaxDist = 2
        self.debug = debug
        self.TGtime = 5
        self.lastTGtofbot = 0
        self.pings = {}
        self.memoryDepth = 20
        self.lolRateDepth = 8
        self.msgMemory = []
        self.plugins = self.load_plugins()

    def load_plugins(self):
        d = os.path.dirname(__file__)
        plugindir = os.path.join(d, 'plugins')
        plugin_instances = []
        for m in dir(plugins):
            if type(getattr(plugins,m)) != types.ModuleType:
                continue
            plugin = getattr(plugins, m)
            for n in dir(plugin):
                c = getattr(plugin, n)
                if type(c) != types.ClassType:
                    continue
                if c.__name__.startswith('Plugin'):
                    instance = c(self)
                    plugin_instances.append(instance)
        return plugin_instances

    # line-feed-safe
    def msg(self, chan, msg):
        for m in msg.split("\n"):
            Bot.msg(self, chan, m)
        
    def log(self, msg):
        if self.debug:
            print(msg)

    def try_join(self, args):
        if (args[0] in ['End of /MOTD command.',
                        "This server was created ... I don't know"]
                        ):
            for chan in self.channels:
                self.write(('JOIN', chan))
            self.joined = True


    def dispatch(self, origin, args):
        self.log("o=%s n=%s a=%s" % (origin.sender, origin.nick, args))
        
        senderNick = origin.nick
        commandType = args[1]

        if not self.joined:
            self.try_join(args)
            return

        if commandType == 'JOIN':
            chan = args[0]
            if senderNick == self.nick:
                self.cmd_tofade(chan, [])
            else:
                self.cmd_tofme(chan, [senderNick])
        
        elif commandType == 'KICK' and args[0] == self.nick:
            chan = args[2]
            self.write(('JOIN', chan))
            self.msg(chan, 'respawn, LOL')

        elif commandType == 'PRIVMSG':
            msg_text = args[0]
            msg = msg_text.split(" ")
            cmd = msg[0]
            chan = args[2]
            
            self.pings[senderNick] = datetime.now()
            
            if msg_text.strip() == "TG " + self.nick:
                self.lastTGtofbot = time.time()

            if msg_text.strip() == "GG " + self.nick:
                self.lastTGtofbot = 0

            if (random.randint(0, 100) > self.autoTofadeThreshold and 
                (time.time() - self.lastTGtofbot) >= (self.TGtime * 60)):
                self.cmd_tofme(chan, [senderNick])
                
            if self.active_riddle():
                itsOver = self.devinette.wait_answer(chan, msg_text)
                if itsOver:
                    self.devinette = None

            if len(cmd) == 0:
                return

            for p in self.plugins:
                if hasattr(p, 'handle_msg'):
                    p.handle_msg(msg_text)

            if chan == self.channels[0] and cmd[0] != '!':
                self.msgMemory.append("<" + senderNick + "> " + msg_text)
                if len(self.msgMemory) > self.memoryDepth:
                    del self.msgMemory[0]

            if cmd[0] != '!':
                return
            
            cmd = cmd[1:]

            if cmd in _simple_dispatch:
                self.call_cmd_action("cmd_" + cmd, msg[1:])
            elif cmd == 'context':
                self.send_context(senderNick)

    def call_cmd_action(self, cmd_name, args):
        targets = self.plugins
        targets.insert(0, self)
        found = False

        for t in targets:
            if (hasattr(t, cmd_name)):
                action = getattr(t, cmd_name)
                action(self.channels[0], args)
                break

    def safe_getattr(self, key):
        if key not in self._mutable_attributes:
            return None
        if not hasattr(self, key):
            return "(None)"
        else:
            return str(getattr(self, key))

    def safe_setattr(self, key, value):
        try:
            converter = self._mutable_attributes.get(key)
            if converter is None:
                return False
            value = converter(value)
            setattr(self, key, value)
            return True
        except ValueError:
            pass

    def active_riddle(self):
        return (hasattr(self, 'devinette') and self.devinette is not None)
    
    @cmd(1)
    def cmd_ping(self, chan, args):
        who = args[0]
        if who in self.pings:
            self.msg(chan, 
                "Last message from %s was on %s (btw my local time is %s)" % 
                (who, self.pings[who].__str__(), datetime.now().__str__() ))
        else:
            self.msg(chan, "I havn't seen any message from " + who)

    @cmd(0)
    def cmd_blague(self, chan, args):
        self.msg(chan, self._jokes())

    @cmd(0)
    def cmd_fortune(self, chan, args):
        self.msg(chan, self._fortunes())

    @cmd(0)
    def cmd_chuck(self, chan, args):
        self.msg(chan, self._chuck())

    @cmd(0)
    def cmd_tofade(self, chan, args):
        self.msg(chan, self._tofades())
            
    @cmd(0)
    def cmd_contrepetrie(self, chan, args):
        self.msg(chan, self._contrepetries())

    @cmd(1)
    def cmd_tofme(self, chan, args):
        who = args[0]
        self.msg(chan, "%s : %s" % (who, self._tofades()))

    @cmd(0)
    def cmd_devinette(self, chan, args):
        if not self.active_riddle():
            self.devinette = self.random_riddle(chan)

    @cmd(1)
    def cmd_get(self, chan, args):
        key = args[0]
        value = self.safe_getattr(key)
        if value is None:
            self.msg(chan, "Ne touche pas à mes parties privées !")
        else:
            self.msg(chan, "%s = %s" % (key, value))

    @cmd(2)
    def cmd_set(self, chan, args):
        key = args[0]
        value = args[1]
        ok = self.safe_setattr(key, value)
        if not ok:
            self.msg(chan, "N'écris pas sur mes parties privées !")

    def send_context(self, to):
        intro = "Last " + str(len(self.msgMemory)) + " messages sent on " + self.channels[0] + " :"
        self.msg(to, intro)
        
        for msg in self.msgMemory:
            self.msg(to, msg)

    @cmd(0)
    def cmd_help(self, chan, args):
        commands = ['!' + cmd for cmd in _simple_dispatch]
        commands.append("!context")
        self.msg(chan, "Commands should be entered in the channel or by private message")
        self.msg(chan, "Available commands : " + ' '.join(commands))
        self.msg(chan, "you can also !get or !set " + ", ".join(self._mutable_attributes.keys()))
        self.msg(chan, "If random-tofades are boring you, enter 'TG " + self.nick + "' (but can be cancelled by GG " + self.nick + ")")

    def random_riddle(self, chan):
        riddle = self._riddles()
        r = RiddleTeller (riddle,
                          chan,
                          lambda msg: self.msg(chan, msg),
                          self.riddleMaxDist)
        return r

if __name__ == "__main__":
    if len(sys.argv) > 2:
        chans = [ "#" + s for s in sys.argv[2:] ]
        b = Tofbot(sys.argv[1], 'Tofbot', chans)
        b.run('irc.freenode.net')
    else:
        print __doc__
