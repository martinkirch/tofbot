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
