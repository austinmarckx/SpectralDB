import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from itertools import chain
from typing import Optional, Literal, Union, NamedTuple
from spectraldb.utils.types import (
    CIE_XYZ, RGB, Color, RGBTuple, ColorRange, Wavelength, Element, Illuminant, RGB_WORKING_SPACE
    )
from spectraldb.utils.misc import minmaxnorm
from spectraldb.models.wss import WSS
from spectraldb.models.lindbloom import get_working_space
from spectraldb.utils.preprocess import preprocess, filter_visible



def make_elemental_colorscale(el:Optional[Union[Element, list[Element]]]=None):
    if isinstance(el, str):
        el = [el]
    df = pd.concat([ filter_visible(preprocess(e, trimmed=True, xyz=True))for e in el], axis=0, ignore_index=True)
    cs = set([v[1] for v in make_colorscale(df.reset_index(drop=True).sort_values(by="wavelength_nm"))])
    cs = [v.tostr() for v in sorted(map(Color.totuple, cs), key=lambda t: (sum(t), t[0], t[1], t[2]) ) ]
    return cs 


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
    # Delete duplicate color entries:
    # colorscale = [colorscale[idx] for idx in range(len(colorscale)) if colorscale[idx][1] != colorscale[idx-1][1]]
    #colorscale[-1] = (1.0, colorscale[-1][1])
    return colorscale

def cmap_handler(cmap:str, lower:float=0.0, upper: float=1.0, n: int=100):
    # https://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib
    def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
        new_cmap = colors.LinearSegmentedColormap.from_list(
            'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
            cmap(np.linspace(minval, maxval, n)))
        return new_cmap
    return truncate_colormap(plt.get_cmap(cmap), lower, upper, n)

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
    return RGB_to_Color(XYZ_to_RGB(val))

def RGB_to_Color(RGB:RGB) -> Color:
    """ Translate RGB into closest renderable color 
    RGB can contain negative values from colorspace conversion which cannot be rendered.
    """
    convert = lambda val: max(0, min(round(val*255),255))
    return Color(rgb=(convert(RGB.r), convert(RGB.g), convert(RGB.b)) )




def XYZ_to_RGB(val:CIE_XYZ, space:Literal[RGB_WORKING_SPACE]="CIE_RGB") -> RGB:
    space = get_working_space(space)
    rgb = (val.to_numpy() @ space.M_inv).tolist()
    return RGB(rgb[0], rgb[1], rgb[2])

def RGB_to_XYZ(val:RGB, space:Literal[RGB_WORKING_SPACE]="CIE_RGB") -> CIE_XYZ:
    space = get_working_space(space)
    XYZ = (val.to_numpy() @ space.M).tolist()
    return CIE_XYZ(XYZ[0], XYZ[1], XYZ[2])


