
import os
import pandas as pd

from spectraldb.utils.defaults import RAW_LINES_PATH, ELEMENTS, ELEMENTS_R
from spectraldb.utils.types import Element, InvalidElementError, CIEReference
from typing import Optional, Union, Literal

def load_cie_reference(ref:Literal["1931", "2006"]="2006", deg:Literal["2","10"]="2", refdeg:Optional[CIEReference]=None):
    if refdeg is not None:
        ref, deg = refdeg.split("_deg")

    df = None
    if ref == "1931" and deg == "2":
        df = pd.read_csv("data\\CIE\\CIE_xyz_1931_2deg.csv", header=None, names=["wavelength_nm","x","y","z"])
    elif ref == "2006" and deg == "2":
        df = pd.read_csv("data\\CIE\\lin2012xyz2e_fine_7sf.csv", header=None, names=["wavelength_nm","x","y","z"])
    elif ref == "2006" and deg == "10":
        df = pd.read_csv("data\\CIE\\lin2012xyz10e_fine_7sf.csv", header=None, names=["wavelength_nm","x","y","z"])
    else:
        raise ValueError("Invalid ref/deg combination")
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
