# those commands directly trigger cmd_* actions
_simple_dispatch = set()

def cmd(expected_args):
    def deco(func):
        name = func.__name__[4:]
        _simple_dispatch.add(name)
        def f(bot, chan, args):
            if(len(args) == expected_args):
                return func(bot, chan, args)
        return f
    return deco
