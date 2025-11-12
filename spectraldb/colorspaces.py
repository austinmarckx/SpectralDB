import pandas as pd
import numpy as np
from itertools import chain
from typing import Optional, Literal, Union
from spectraldb.utils.types import CIE_XYZ, sRGB, Color, RGBTuple, ColorRange, Wavelength
from spectraldb.utils.misc import minmaxnorm
from spectraldb.models.wss import WSS

def make_colorscale(df:pd.DataFrame, norm_col:str="wl_norm", color_col:str="color") -> list[ColorRange]:
    if norm_col not in df.columns:
        df[norm_col] = normalize_wavelength(df)
    if color_col not in df.columns:
        df[color_col] = add_color_col(df)
    
    func = lambda idx: {
        "lower":df[norm_col][idx-1] if idx > 1 else 0.,
        "upper":df[norm_col][idx],
        "r":df[color_col][idx][0],
        "g":df[color_col][idx][1],
        "b":df[color_col][idx][2],
    }
    colorscale = sorted(set(chain.from_iterable([ ColorRange(**func(i)).to_colorscale() for i in range(1, df.shape[0])] ) ))
    return colorscale



def add_color_col(df:pd.DataFrame, xcol:str="x", ycol:str="y", zcol:str="z", deg:Optional[Literal["2","10"]]=None) -> list[RGBTuple]:    
    func = lambda x,y,z: XYZ_to_color(CIE_XYZ(x,y,z,deg=deg))[0]
    return [func(x,y,z) for x,y,z in zip(df[xcol], df[ycol], df[zcol])] 

def normalize_wavelength(df:pd.DataFrame, col:str="wavelength_nm") -> list[float]:
    return minmaxnorm(df.sort_values(by=col,ascending=True)[col].tolist()) 

def wavelength_to_XYZ(val:Union[float,Wavelength], **kwargs) -> CIE_XYZ:
    return WSS.fit(val, **kwargs)

def wavelength_to_color(val:Union[float,Wavelength]) -> Color:
    return XYZ_to_color(wavelength_to_XYZ(val))

def XYZ_to_color(val:CIE_XYZ) -> Color:
    return sRGB_to_Color(XYZ_to_sRGB(val))

def sRGB_to_Color(srgb:sRGB) -> Color:
    """ Translate sRGB into closest renderable color 
    sRGB can contain negative values from colorspace conversion which cannot be rendered.
    """
    convert = lambda val: max(0, min(round(val*255),255))
    return Color(rgb=(convert(srgb.r), convert(srgb.g), convert(srgb.b)) )

def XYZ_to_sRGB(val:CIE_XYZ) -> sRGB:
    M_inv = np.matrix([
        [2.3644, -0.8958, -0.4686],
        [-0.5148, 1.4252, 0.0896],
        [0.0052, -0.0144, 1.0092],
    ])
    rgb = (np.array([val.x, val.y, val.z]) @ M_inv).tolist()
    return sRGB(rgb[0][0], rgb[0][1], rgb[0][2])

def sRGB_to_XYZ(val:sRGB) -> CIE_XYZ:
    M = np.matrix([
        [0.490, 0.310, 0.200],
        [0.177, 0.813, 0.010],
        [0.000, 0.010, 0.990],
    ])
    XYZ = (np.array([val.r, val.g, val.b]) @ M).tolist()
    return CIE_XYZ(XYZ[0][0], XYZ[0][1], XYZ[0][2], "2")