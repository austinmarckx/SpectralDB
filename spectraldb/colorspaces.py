import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from itertools import chain
from typing import Optional, Literal, Union
from spectraldb.utils.types import CIE_XYZ, sRGB, Color, RGBTuple, ColorRange, Wavelength, Element
from spectraldb.utils.misc import minmaxnorm
from spectraldb.models.wss import WSS
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