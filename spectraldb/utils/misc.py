
def minmaxnorm(ls:list[float]) -> float:
    """ Normalize list entries between 0 and 1 """
    mn, mx = min(ls), max(ls)
    func = lambda val: (val - mn) / (mx-mn)
    return list(map(func, ls))


def nothing_burger(*args, **kwargs):
    """Prints args and kwargs. Intended as placeholder for callables"""
    func = lambda *args, **kwargs: f"Callable\n\tArgs: {args}\n\tKwargs: {kwargs}"
    return func(*args, **kwargs)

def uno_reverse(*args, **kwargs):
    """An even more elaborate pass through"""
    out = None
    if len(args) and not len(kwargs):
        out = args if len(args) > 1 else args[0]
    elif len(args) and len(kwargs):
        out = args, kwargs
    elif not len(args) and len(kwargs):
        out = kwargs
    elif not len(args) and not len(kwargs):
        pass 
    return out



