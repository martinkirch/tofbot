#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2011 Etienne Millon <etienne.millon@gmail.com>
#                    Martin Kirchgessner <martin.kirch@gmail.com>
#                    Nicolas Dumazet <nicdumz.commits@gmail.com>
#                    Quentin Sabah <quentin.sabah@gmail.com>

"""
./bot.py [options] [legacy-arguments]

Legacy-arguments:
  NICK CHANNEL [CHANNEL...]

  Don't prepend a # to chan names
  Tofbot will connect to freenode.net
"""

from datetime import datetime
from irc import Bot
import time
import random
import sys
import os
import plugins
import types
from toflib import *
from toflib import _simple_dispatch, _simple_conf_dispatch
import re
from optparse import OptionParser
import json
import atexit
import socket

import plugins.euler
import plugins.lolrate
import plugins.donnezmoi
import plugins.jokes
import plugins.twitter
import plugins.dassin
import plugins.eightball
import plugins.teachme
import plugins.sed
import plugins.rick

random.seed()

class AutosaveEvent(CronEvent):

    def __init__(self, bot, filename):
        CronEvent.__init__(self, None)
        self.filename = filename
        self.bot = bot

    def fire(self):
        self.bot.save(self.filename)

class Tofbot(Bot):

    # Those attributes are published and can be changed by irc users
    # value is a str to object converter. It could do sanitization:
    # if value is incorrect, raise ValueError
    _mutable_attributes = {
        "TGtime":int,
        "memoryDepth":int
    }

    def __init__(self, nick=None, name=None, channels=None, password=None, debug=True):
        Bot.__init__(self, nick, name, channels, password)
        self.joined = False
        self.autoTofadeThreshold = 98
        self.riddleMaxDist = 2
        self.debug = debug
        self.TGtime = 5
        self.pings = {}
        self.memoryDepth = 20
        self.lolRateDepth = 8
        self.msgMemory = []
        self.cron = Cron()
        self.plugins = self.load_plugins()

    def run(self, host=None):
      if host == None and not hasattr(self,'host'):
        raise Exception("run: no host set or given")
      if self.nick == None:
        raise Exception("run: no nick set")
      if self.name == None:
        raise Exception("run: no name set")
      self.host = host or self.host
      Bot.run(self, self.host)

    def load_plugins(self):
        d = os.path.dirname(__file__)
        plugindir = os.path.join(d, 'plugins')
        plugin_instances = {}
        for m in dir(plugins):
            if type(getattr(plugins,m)) != types.ModuleType:
                continue
            plugin = getattr(plugins, m)
            for n in dir(plugin):
                c = getattr(plugin, n)
                if type(c) not in [types.ClassType, types.TypeType]:
                    continue
                name = c.__name__
                if name.startswith('Plugin'):
                    instance = c(self)
                    plugin_name = name[6:].lower()
                    plugin_instances[plugin_name] = instance
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

        is_config = False
        senderNick = origin.nick
        commandType = args[1]

        # if command type is 'BOTCONFIG', bypass the try_join
        # because we are configuring the bot before any
        # connection.
        if commandType != 'BOTCONFIG':
            if not self.joined:
                self.try_join(args)
                return
        else:
            is_config = 1
            args.remove('BOTCONFIG')
            commandType = args[1]

        if commandType == 'JOIN':
            for p in self.plugins.values():
                if hasattr(p, 'handle_join'):
                    p.handle_join(args[0], senderNick)

        elif commandType == 'KICK' and args[3] == self.nick:
            reason = args[0]
            chan = args[2]
            if reason == self.nick:
                respawn_msg = 'respawn, LOL'
            else:
                respawn_msg = 'comment ça, %s ?' % reason
            self.write(('JOIN', chan))
            self.msg(chan, respawn_msg)

        elif commandType == 'PRIVMSG':
            msg_text = args[0]
            msg = msg_text.split(" ")
            cmd = msg[0]
            chan = args[2]

            self.pings[senderNick] = datetime.now()

            if is_config == False:
                self.cron.tick()

                if len(cmd) == 0:
                    return
               
                for p in self.plugins.values():
                    if hasattr(p, 'handle_msg'):
                        p.handle_msg(msg_text, chan, senderNick)

                if chan == self.channels[0] and cmd[0] != '!':
                    self.msgMemory.append("<" + senderNick + "> " + msg_text)
                    if len(self.msgMemory) > self.memoryDepth:
                        del self.msgMemory[0]

            if len(cmd) == 0 or cmd[0] != '!':
                return

            cmd = cmd[1:]

            chan = None
            if len(self.channels) == 0:
              chan = 'config'
            else:
              chan = self.channels[0]

            if cmd in _simple_dispatch:
                act = self.find_cmd_action("cmd_" + cmd)
                act(chan, msg[1:])
            elif is_config and (cmd in _simple_conf_dispatch):
              act = self.find_cmd_action("confcmd_" + cmd)
              act(chan, msg[1:])
            elif cmd == 'context':
                self.send_context(senderNick)

        else: # Unknown command type
            self.log('Unknown command type : %s' % commandType)

    def find_cmd_action(self, cmd_name):
        targets = self.plugins.values()
        targets.insert(0, self)

        for t in targets:
            if (hasattr(t, cmd_name)):
                action = getattr(t, cmd_name)
                return action

        def nop(self, chan, args):
            pass

        return nop

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

    @confcmd(1)
    def confcmd_chan(self, chan, args):
      new_chan = args[0]
      if self.channels.count(new_chan) == 0:
        self.channels.append(new_chan)

    @confcmd(1)
    def confcmd_server(self, chan, args):
      host = args[0].strip()
      self.host = host

    @confcmd(1)
    def confcmd_port(self, chan, args):
      port = int(args[0].strip())
      self.port = port

    @confcmd(1)
    def confcmd_nick(self, chan, args):
      nick = args[0].strip()
      self.nick = nick
      self.user = nick

    @confcmd(1)
    def confcmd_name(self, chan, args):
      name = args[0].strip()
      self.name = name

    @cmd(1)
    def cmd_ping(self, chan, args):
        "Find when X was last online"
        who = args[0]
        if who in self.pings:
            self.msg(chan,
                "Last message from %s was on %s (btw my local time is %s)" %
                (who, self.pings[who].__str__(), datetime.now().__str__() ))
        else:
            self.msg(chan, "I havn't seen any message from " + who)

    @cmd(1)
    def cmd_get(self, chan, args):
        "Retrieve a configuration variable's value"
        key = args[0]
        value = self.safe_getattr(key)
        if value is None:
            self.msg(chan, "Ne touche pas à mes parties privées !")
        else:
            self.msg(chan, "%s = %s" % (key, value))

    @cmd(2)
    def cmd_set(self, chan, args):
        "Set a configuration variable's value"
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
        "Show this help message"
        maxlen = 1 + max(map(len, _simple_dispatch))

        self.msg(chan, "Commands should be entered in the channel or by private message")
        for cmd in _simple_dispatch:
            f = self.find_cmd_action("cmd_" + cmd)
            self.msg(chan, '%*s - %s' % (maxlen, "!"+cmd, f.__doc__))
        self.msg(chan, "you can also !get or !set " + ", ".join(self._mutable_attributes.keys()))
        self.msg(chan, "If random-tofades are boring you, enter 'TG " + self.nick + "' (but can be cancelled by GG " + self.nick + ")")

    def load(self, filename):
        with open(filename) as f:
            state = json.load(f)
            if state['version'] != 1:
                return False
            for name, plugin_state in state['plugins'].items():
                plugin = self.plugins[name]
                plugin.load(plugin_state)

    def save(self, filename):
        with open(filename, 'w') as f:
            state = { 'version': 1
                    , 'plugins': {}
                    }
            for name, plugin in self.plugins.items():
                plugin_state = plugin.save()
                state['plugins'][name] = plugin_state
            json.dump(state, indent=4, fp=f)

if __name__ == "__main__":
    class FakeOrigin:
      pass

    def bot_config(b, cmd):
      o = FakeOrigin
      o.sender = 'bot_config'
      o.nick = 'bot_config'
      b.dispatch(o, [cmd.strip(), 'BOTCONFIG','PRIVMSG','#bot_config'])

    # default timeout for urllib2, in seconds
    socket.setdefaulttimeout(15)

    # option parser
    parser = OptionParser(__doc__)
    parser.add_option("-x","--execute", dest="cmds",action="append",help="File to execute prior connection. Can be used several times.")
    parser.add_option("-s","--host", dest="host",help="IRC server hostname")
    parser.add_option("-p","--port", dest="port",help="IRC server port")
    parser.add_option("-k","--nick", dest="nick",help="Bot nickname",default='Tofbot')
    parser.add_option("-n","--name", dest="name",help="Bot name",default='Tofbot')
    parser.add_option("-c","--channel",dest="channel",action="append",help="Channel to join (without # prefix). Can be used several times.")
    parser.add_option("--password", dest="password")
    parser.add_option("-d","--debug", action="store_true", dest="debug", default=False)

    (options,args) = parser.parse_args();

    # legacy arguments handled first
    # (new-style arguments prevail)
    if len(args) > 0:
      options.nick = options.nick or args[0]
      options.channel = options.channel or []
      for chan in args[1:]:
        if options.channel.count(chan) == 0:
          options.channel.append(chan)

    # initialize Tofbot
    # using command-line arguments
    b = Tofbot(options.nick, options.name, options.channel, options.password, options.debug)

    # execute command files
    # these commands may override command-line arguments
    options.cmds = options.cmds or []
    for filename in options.cmds:
      cmdsfile = open(filename,'r')
      for line in cmdsfile:
        bot_config(b, line)

    # Restore serialized data
    state_file = "state.json"
    if os.path.isfile(state_file):
        b.load(state_file)

    # Perform auto-save periodically
    autosaveEvent = AutosaveEvent(b, state_file)
    b.cron.schedule(autosaveEvent)

    # ... and save at exit
    @atexit.register
    def save_atexit():
        print("Exiting, saving state...")
        b.save(state_file)
        print("Done !")

    # default host when legacy-mode
    if options.host == None and len(options.cmds) == 0 and len(args) > 0:
      options.host = 'irc.freenode.net'

    b.run(options.host)

