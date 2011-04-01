from testbot import TestTofbot, print_resp
import random

class Origin:
    pass

chan = '#test'

origin = Origin()
origin.sender = 'TestTofbot'
origin.nick = 'TestTofbot_nick'

class Counter:
    
    def __init__(self, n):
        self.remaining_calls = n

    def __call__(self, msg):
        print_resp(msg)
        self.remaining_calls -= 1
        if self.remaining_calls < 0:
            assert False

def cb_lines(n):
    return Counter(n)

def cb_error(msg):
    return cb_lines(0)

b = TestTofbot('ohohOHoh_bot', 'Le tof', chan, origin)
random.seed(0) # be deterministic

b.send("End of /MOTD command.", cb=cb_error)
b.send("test", cb=cb_error)
b.send("!help", cb=cb_lines(4))
b.send("!set autoTofadeThreshold 100", cb=cb_error)
b.send("!get autoTofadeThreshold", cb=cb_lines(1))
b.send("!get autoTofadeThreshold 2", cb=cb_error)
b.send("!devinette")
b.send("idk", cb=cb_error)
b.send("idk", cb=cb_error)
b.send("idk", cb=cb_lines(1))
b.send("!devinette", cb=cb_error)
b.send("parce que george bushe", cb=cb_lines(1))
b.send("!set lol 2", cb=cb_lines(1))
