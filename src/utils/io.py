
import os
import pandas as pd

from .defaults import RAW_LINES_PATH, ELEMENTS, ELEMENTS_R
from .types import Element, InvalidElementError
from typing import Optional, Union

def system_agnostic_pathjoin(path:Union[str,list], root:Optional[Union[str,list]]=None):
    if root is None:
        root = os.getcwd().split(os.path.sep)
    if isinstance(root, str):
        root = root.split(os.path.sep)

    if isinstance(path, str):
        path = [path]

    return os.path.sep.join(root + path)

def process_element_abbreviation(abbr:str) -> str:
    if abbr in ELEMENTS_R:
        return ELEMENTS_R[abbr]
    return abbr.lower().capitalize()[:min(2, len(abbr))]


def load_element(el:Element, suffix:str=".csv") -> pd.DataFrame:
    """ 
    Takes an element Abbreviation and loads the data from disk.
    """
    el = process_element_abbreviation(el)
    if el not in ELEMENTS:
        raise InvalidElementError(f"{el} is not a recongized element. Currently accepted elements are: {ELEMENTS}")

    df = None
    try:
        df = pd.read_csv(system_agnostic_pathjoin([el+suffix], root=RAW_LINES_PATH))
        # Raw data has extra column, by default. Drop it.
        df = df.iloc[:,:-1]
    except Exception as e:
        raise e(f"Unable to load data for element: {el}")

    return df
