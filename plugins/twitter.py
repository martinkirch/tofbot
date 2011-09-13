from datetime import datetime, timedelta
from toflib import cmd
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

class PluginTwitter:

    def __init__(self, bot):
        self.bot = bot
        self.user = None
        self.tweet = None
        self.time = datetime.min
        self.frequency = timedelta(minutes=10)

    def handle_msg(self, msg_text, chan):
        if self.user is not None and datetime.now() - self.time > self.frequency:
            tweet = lastTweet(self.user)
            if tweet is not None and tweet != self.tweet:
                self.tweet = tweet
                self.bot.msg(chan, "@%s: %s" % (self.user, tweet))

    @cmd(1)
    def cmd_twitter_track(self, chan, args):
        user = args[0]
        self.user = user
        self.time = datetime.min
