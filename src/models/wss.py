""" Wymann, Sloan, and Shirley (WSS) Analytic approximations of CIE XYZ Color matching functions

Access link:
https://jcgt.org/published/0002/02/01/paper.pdf

Citation:
@inproceedings{Wyman2013SimpleAA,
  title={Simple Analytic Approximations to the CIE XYZ Color Matching Functions},
  author={Chris Wyman and Peter-Pike J. Sloan and Peter Shirley},
  year={2013},
  url={https://api.semanticscholar.org/CorpusID:3343179}
}
"""
import numpy as np
from typing import Literal, Union
from ..utils.types import CIE_XYZ, Wavelength
from ..utils.defaults import LRU_CACHE_SIZE
from functools import lru_cache

def replacena(val:float) -> float:
    return val if not np.isnan(val) else 0.

def x31_simple_single_lobe_deg2(wl:float) -> float:
    return ( 
        1.065*np.exp((-0.5*( (wl-595.8)/33.33 )**2 ))  
        + 0.366*np.exp((-0.5*( (wl-446.8)/19.44 )**2 ))
    )

def y31_simple_single_lobe_deg2(wl:float) -> float:
    return ( 1.014*np.exp((-0.5*( ( np.log(wl)-np.log(556.3))/0.075 )**2 )) )

def z31_simple_single_lobe_deg2(wl:float) -> float:
    return ( 1.839*np.exp((-0.5*( ( np.log(wl)-np.log(449.8))/0.051 )**2 )) )

def x64_simple_single_lobe_deg10(wl:float) -> float:
    return ( 
        0.398*np.exp( -1250*( (np.log( (wl+570.1)/1014 )**2) ) )
        + 1.132*np.exp( -234*( (np.log( (1338-wl)/743.5 )**2) ) )
    )

def y64_simple_single_lobe_deg10(wl:float) -> float:
    return ( 1.011*np.exp((-0.5*( ( wl-556.1)/46.14 )**2 )) )

def z64_simple_single_lobe_deg10(wl:float) -> float:
    return ( 2.060*np.exp(-32*( (np.log( ( wl-265.8)/180.4))**2 )) )

def x31_multi_lobe_deg2(wl:float) -> float:
    t1 = (wl-442.0) * (0.0624 if wl < 442.0 else 0.0374)
    t2 = (wl-599.8) * (0.0264 if wl < 599.8 else 0.0323)
    t3 = (wl-501.1) * (0.0490 if wl < 501.1 else 0.0382)
    return (0
        + 0.362*np.exp(-0.5*t1*t1)
        + 1.056*np.exp(-0.5*t2*t2)
        - 0.065*np.exp(-0.5*t3*t3)
    )

def y31_multi_lobe_deg2(wl:float) -> float:
    t1 = (wl-568.8) * (0.0213 if wl < 568.8 else 0.0247)
    t2 = (wl-530.9) * (0.0613 if wl < 530.9 else 0.0322)
    return (0
        + 0.821*np.exp(-0.5*t1*t1)
        + 0.286*np.exp(-0.5*t2*t2)
    )

def z31_multi_lobe_deg2(wl:float) -> float:
    t1 = (wl-437.0) * (0.0845 if wl < 437.0 else 0.0278)
    t2 = (wl-459.0) * (0.0385 if wl < 459.0 else 0.0725)
    return (0
        + 1.217*np.exp(-0.5*t1*t1)
        + 0.681*np.exp(-0.5*t2*t2)
    )


@lru_cache(LRU_CACHE_SIZE)
def simple_single_lobe_deg2(lam:Union[float,Wavelength], zero_nas:bool=True) -> CIE_XYZ:
    """ 2degree CIE 1931 standard observer """
    if not isinstance(lam, Wavelength):
        lam = Wavelength(lam)
    x31 = x31_simple_single_lobe_deg2(lam.wl)
    y31 = y31_simple_single_lobe_deg2(lam.wl)
    z31 = z31_simple_single_lobe_deg2(lam.wl)
    
    if zero_nas:
        x31 = replacena(x31)
        y31 = replacena(y31)
        z31 = replacena(z31)

    return CIE_XYZ(x31, y31, z31, 2)

@lru_cache(LRU_CACHE_SIZE)
def simple_single_lobe_deg10(lam:Union[float,Wavelength], zero_nas:bool=True) -> CIE_XYZ:
    """ 10 degree CIE 1964 standard observer """
    if not isinstance(lam, Wavelength):
        lam = Wavelength(lam)
    x64 = x64_simple_single_lobe_deg10(lam.wl)
    y64 = y64_simple_single_lobe_deg10(lam.wl)
    z64 = z64_simple_single_lobe_deg10(lam.wl)

    if zero_nas:
        x64 = replacena(x64)
        y64 = replacena(y64)
        z64 = replacena(z64)
    return CIE_XYZ(x64, y64, z64, 10)

@lru_cache(LRU_CACHE_SIZE)
def multi_lobe_deg2(lam:Union[float,Wavelength], zero_nas:bool=True) -> CIE_XYZ:
    """ 2degree CIE 1931 standard observer """
    if not isinstance(lam, Wavelength):
        lam = Wavelength(lam)
    x31 = x31_multi_lobe_deg2(lam.wl)
    y31 = y31_multi_lobe_deg2(lam.wl)
    z31 = z31_multi_lobe_deg2(lam.wl)
        
    if zero_nas:
        x31 = replacena(x31)
        y31 = replacena(y31)
        z31 = replacena(z31)

    return CIE_XYZ(x31, y31, z31, 2)



class WSS:
    """ Wymann, Sloan, and Shirley (WSS) Analytic approximations of CIE XYZ Color matching functions"""
    def __init__(self):
        pass
    
    @classmethod
    def fit(cls, lam:Union[float,Wavelength], how:Literal["simple", "multi"]="multi", deg:Literal["2", "10"]="2"):
        ans = None
        if how == "simple" and deg == "2":
            ans = simple_single_lobe_deg2(lam)
        elif how == "simple" and deg == "10":
            ans = simple_single_lobe_deg10(lam)
        elif how == "multi" and deg == "2":
            ans = multi_lobe_deg2(lam)
        else:
            raise ValueError("Invalid combination of `how` and `deg`")

        return ans