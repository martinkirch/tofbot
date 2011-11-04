# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2011 Etienne Millon <etienne.millon@gmail.com>
#                    Christophe-Marie Duquesne <chm.duquesne@gmail.com>

"See PluginTwitter"
from toflib import cmd, Plugin, CronEvent
import json
import urllib2

def last_tweet(user):
    """
    Returns the last tweet of the given user (None if problem)
    """
    request = "http://api.twitter.com/1/users/show.json?screen_name=" + user
    try:
        answer = urllib2.urlopen(request)
        answer_data = json.load(answer)
        return answer_data["status"]["text"]
    except: # too many things can go wrong to catch explicitly
        return None

class TweetEvent(CronEvent):
    """
    Polls twitter every default period.
    If the last tweet is different from last time, print it !
    """

    def __init__(self, plugin, user):
        CronEvent.__init__(self, plugin)
        self.user = user
        self.previous_tweet = None

    def fire(self):
        print "%s fire()" % self
        tweet = last_tweet(self.user)
        if tweet is None:
            return
        if tweet != self.previous_tweet:
            self.plugin.say("@%s: %s" % (self.user, tweet))
            self.previous_tweet = tweet

class PluginTwitter(Plugin):
    """
    A twitter client plugin.
    It is possible to follow users with the 'twitter_track' command.
    """

    def __init__(self, bot):
        Plugin.__init__(self, bot)

    @cmd(1)
    def cmd_twitter_track(self, _chan, args):
        "Follow a user on twitter"
        user = args[0]
        event = TweetEvent(self, user)
        self.bot.cron.schedule(event)
