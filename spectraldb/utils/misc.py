def nothing_burger(*args, **kwargs):
    """Prints args and kwargs. Intended as placeholder for callables"""
    func = lambda *args, **kwargs: f"Callable\n\tArgs: {args}\n\tKwargs: {kwargs}"
    return func(*args, **kwargs)