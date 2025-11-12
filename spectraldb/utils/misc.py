import random
import pandas as pd
from typing import Union
from spectraldb.utils.types import Wavelength

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

def select_random_wavelengths(df:pd.DataFrame, n:int=1, col:str="wavelength_nm") -> Union[list[Wavelength], Wavelength]:
    chosen = random.sample(df[col].to_list(), n)
    waves = list(map(Wavelength, chosen))
    if len(waves) > 1:
        return waves
    return waves[0]


