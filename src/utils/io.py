
import os
import pandas as pd

from defaults import SPECTRALDB_ABS_PATH, RAW_LINES_PATH
from utils.types import Element, InvalidElementError
from typing import Optional, Union, get_args

def system_agnostic_pathjoin(path:Union[str,list], root:Optional[Union[str,list]]=None):
    if root is None:
        root = os.getcwd().split(os.path.sep)
    if isinstance(root, str):
        root = root.split(os.path.sep)

    if isinstance(path, str):
        path = [path]

    return os.path.sep.join(root + path)

def process_element_abbreviation(abbr:str) -> str:
    return abbr.lower().capitalize()


def load_element(el:Element, suffix:str=".csv") -> pd.DataFrame:
    """ 
    Takes an element Abbreviation and loads the data from disk.
    """
    el = process_element_abbreviation(el)
    if el not in get_args(Element):
        raise InvalidElementError(f"{el} is not a recongized element. Currently accepted elements are: {get_args(Element)}")

    df = None
    try:
        df = pd.read_csv(system_agnostic_pathjoin([el+suffix], root=SPECTRALDB_ABS_PATH))
    except Exception as e:
        raise e(f"Unable to load data for element: {el}")

    return df
