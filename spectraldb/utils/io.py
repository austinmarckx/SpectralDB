
import os
import pandas as pd
from functools import lru_cache
from spectraldb.utils.defaults import RAW_LINES_PATH, ELEMENTS, ELEMENTS_R, CIE_BASE_PATH
from spectraldb.utils.types import Element, InvalidElementError, CIEReference
from typing import Optional, Union, Literal


join_cie = lambda v: os.path.sep.join([CIE_BASE_PATH, v])
CIE_LIST = list(map(join_cie, [
    "CIE_xyz_1931_2deg.csv",
    "lin2012xyz2e_fine_7sf.csv",
    "lin2012xyz10e_fine_7sf.csv",
    "cc2012xyz10_fine_5dp.csv", 
    "linss2_10e_fine.csv", 
]))
CIE_REF_DICT = {idx:fp for idx, fp in enumerate(CIE_LIST)}

@lru_cache(5)
def load_cie_reference(ref:Literal["1931", "2006"]="2006", deg:Literal["2","10"]="2", refdeg:Optional[CIEReference]=None, idx:Optional[int]=None):
    if refdeg is not None:
        ref, deg = refdeg.split("_deg")

    _load = lambda fp: pd.read_csv(fp, header=None, names=["wavelength_nm","x","y","z"]).fillna(0)
    def _parse(ref, deg):
        idx = None
        if ref == "1931" and deg == "2":
            idx = 0
        elif ref == "2006" and deg == "2":
            idx = 1
        elif ref == "2006" and deg == "10":
            idx = 2
        else:
            raise ValueError("Invalid ref/deg combination")
        return idx

    if idx is None:
        idx = _parse(ref, deg)
    
    df = _load(CIE_REF_DICT[idx])
        
    return df

def demo_data() -> pd.DataFrame:
    df = pd.read_csv("data\\demo\\argon_demo.csv", index_col=0)
    return df

def system_agnostic_pathjoin(path:Union[str,list], root:Optional[Union[str,list]]=None):
    if root is None:
        root = os.path.dirname(__file__).split(os.path.sep)[:-2]
    if isinstance(root, str):
        root = root.split(os.path.sep)

    if isinstance(path, str):
        path = [path]

    return os.path.sep.join(root + path)

def lwrcap(s:str):
    """lower case then capitalize input"""
    return s.lower().capitalize()

def process_element_abbreviation(abbr:str) -> str:
    abbr = lwrcap(abbr)
    if abbr in ELEMENTS_R:
        return ELEMENTS_R[abbr]
    return abbr[:min(2, len(abbr))]

def get_element_name(abbr:str) -> str:
    abbr = lwrcap(abbr)
    if abbr in ELEMENTS_R:
        return abbr
    elif abbr in ELEMENTS:
        return ELEMENTS[abbr]
    else:
        raise ValueError("Unrecognized element")



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
