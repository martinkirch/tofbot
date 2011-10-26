from datetime import datetime
from toflib import cmd, Plugin, CronEvent
import json
import urllib2

def lastTweet(user):
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

    def __init__(self, plugin, user):
        CronEvent.__init__(self, plugin)
        self.user = user
        self.previousTweet = None

    def fire(self):
        print "%s fire()" % self
        tweet = lastTweet(self.user)
        if tweet is None:
            return
        if tweet != self.previousTweet:
            self.plugin.say("@%s: %s" % (self.user, tweet))
            self.previousTweet = tweet

class PluginTwitter(Plugin):

    def __init__(self, bot):
        Plugin.__init__(self, bot)

    @cmd(1)
    def cmd_twitter_track(self, chan, args):
        user = args[0]
        ev = TweetEvent(user)
        self.bot.cron.schedule(ev)
