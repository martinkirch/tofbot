import random

# those commands directly trigger cmd_* actions
_simple_dispatch = set()

# those commands directly trigger confcmd_* actions
_simple_conf_dispatch = set()

def cmd(expected_args):
    def deco(func):
        name = func.__name__[4:]
        _simple_dispatch.add(name)
        def f(bot, chan, args):
            if(len(args) == expected_args):
                return func(bot, chan, args)
        f.__doc__ = func.__doc__
        return f
    return deco

def confcmd(expected_args):
  def deco(func):
    name = func.__name__[8:]
    _simple_conf_dispatch.add(name)
    def f(bot, chan, args):
      if(len(args) == expected_args):
        return func(bot, chan, args)
    f.__doc__ = func.__doc__
    return f
  return deco

def distance(string1, string2):
    """
    Levenshtein distance
    http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
    """
    string1 = ' ' + string1
    string2 = ' ' + string2
    dists = {}
    len1 = len(string1)
    len2 = len(string2)
    for i in range(len1):
        dists[i, 0] = i
    for j in range (len2):
        dists[0, j] = j
    for j in range(1, len2):
        for i in range(1, len1):
            if string1[i] == string2[j]:
                dists[i, j] = dists[i-1, j-1]
            else:
                dists[i, j] = min(dists[i-1, j] + 1,
                                  dists[i, j-1] + 1,
                                  dists[i-1, j-1] + 1
                                 )
    return dists[len1-1, len2-1]

class RiddleTeller(object):
    """
    A gentleman (and a scholar) who likes to entertain its audience.
    """

    def __init__(self, riddle, channel, writeback, max_dist):
        self.riddle, self.answer = riddle
        self.channel = channel
        self.writeback = writeback
        self.remaining_msgs = 3
        self.writeback(self.riddle)
        self.max_dist = max_dist

    def wait_answer(self, chan, msg):
        """
        Called at each try.
        Returns True iff the riddle is over.
        """
        if chan != self.channel:
            return False
        if distance(msg.lower(), self.answer.lower()) < self.max_dist:
            self.writeback("10 points pour Griffondor.")
            return True
        self.remaining_msgs -= 1
        if self.remaining_msgs == 0:
            self.writeback(self.answer)
            return True
        return False

class InnocentHand(object):
    """
    A cute 6 years old girl, picking a random object
    from a given pool of candidates
    """
    def __init__(self, pool):
        """
        pool: list of candidates
        """
        self.pool = pool

    def __call__(self, index=None):
        if index:
            return self.pool[index % len(self.pool)]
        random.seed()
        return random.choice(self.pool)

class Plugin(object):

    def __init__(self, bot):
        self.bot = bot

    def say(self, msg):
        self.bot.msg(self.bot.channels[0], msg)
