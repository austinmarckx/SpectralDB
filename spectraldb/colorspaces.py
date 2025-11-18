import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from itertools import chain
from typing import Optional, Literal, Union, NamedTuple
from spectraldb.utils.types import (
    CIE_XYZ, RGB, Color, RGBTuple, ColorRange, Wavelength, Element, 
    Illuminant, StandardIlluminant, RGB_WORKING_SPACE,
    CIE_xyY, CIE_Lab, NamedIlluminant, LCHab, Luv, LCHuv
    )
from spectraldb.illuminant import get_illuminant
from spectraldb.utils.misc import minmaxnorm
from spectraldb.models.wss import WSS
from spectraldb.models.lindbloom import get_working_space
from spectraldb.utils.preprocess import preprocess, filter_visible

WEIN_DISPLACEMENT_CONST_NM = 2_897_771.955185172661
CIE_CORRECTED_EPSILON = 216/24389
CIE_CORRECTED_KAPPA = 24389/27


def wein_approx(wavelength_nm:float) -> float:
    """ Wein's displacement law - input nm - output K"""
    return WEIN_DISPLACEMENT_CONST_NM / wavelength_nm

# def chromaticity_coordinates(wl:Optional[float]=None, temp:Optional[float]=None):
#     assert wl is not None or temp is not None, ValueError("Either wl or temp must be specified")
#     if wl is not None:
#         temp = wein_approx(wl)
    
    




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


def XYZ_to_Luv(val:CIE_XYZ, ill:NamedIlluminant="E") -> Luv:
    if not isinstance(ill, Illuminant):
        ill = get_illuminant(ill)
    
    u_prime = 4*val.x / (val.x + 15*val.y + 3*val.z)
    v_prime = 9*val.y / (val.x + 15*val.y + 3*val.z)
    ur_prime = 4*ill.X / (ill.X + 15*ill.Y + 3*ill.Z)
    vr_prime = 9*ill.Y / (ill.X + 15*ill.Y + 3*ill.Z)

    yr = val.y / ill.Y
    L = CIE_CORRECTED_KAPPA * yr
    if yr > CIE_CORRECTED_EPSILON:
        L = 116*np.cbrt(yr) - 16
    
    u = 13*L*(u_prime - ur_prime)
    v = 13*L*(v_prime - vr_prime)
    return Luv(L, u, v, ill.name)

def Luv_to_XYZ(val:Luv) -> CIE_XYZ:
    ill = val.ill
    if not isinstance(ill, Illuminant):
        ill = get_illuminant(ill)
    u0 = 4*ill.X / (ill.X + 15*ill.Y + 3*ill.Z)
    v0 = 9*ill.Y / (ill.X + 15*ill.Y + 3*ill.Z)

    y = val.L/CIE_CORRECTED_KAPPA
    if val.L > CIE_CORRECTED_KAPPA * CIE_CORRECTED_EPSILON:
        y = ((val.L+16)/116)**3

    a = (1/3)*( (52*val.L) / (val.u + 13*val.L*u0) - 1)
    b = -5*y
    c = -1/3
    d = y*( (39*val.L) / (val.v + 13*val.L*v0) - 5)

    x = (d-b)/(a-c)
    z = (x*a + b)

    return CIE_XYZ(x, y, z)

def Luv_to_LCHuv(val:Luv) -> LCHuv:
    tmp = np.rad2deg(np.atan2(val.v, val.u))
    C = np.sqrt(val.u**2 + val.v**2)
    H = tmp if tmp else 360
    return LCHuv(val.L, C, H, val.ill)

def LCHuv_to_Luv(val:LCHuv) -> Luv:
    u = val.C*np.cos(val.H)
    v = val.C*np.sin(val.H)
    return Luv(val.L, u, v, val.ill)



def XYZ_to_Lab(val:CIE_XYZ, ill:NamedIlluminant="E") -> CIE_Lab:
    if not isinstance(ill, Illuminant):
        ill = get_illuminant(ill)
    xr = val.x / ill.X
    yr = val.y / ill.Y
    zr = val.z / ill.Z

    def eps_func(num:float) -> float:
        if num > CIE_CORRECTED_EPSILON:
            return np.cbrt(num)
        return (CIE_CORRECTED_KAPPA*num + 16)/116
    
    fx, fy, fz = eps_func(xr), eps_func(yr), eps_func(zr)

    L = 116*fy - 16
    a = 500*(fx-fy)
    b = 200*(fy-fz)
    return CIE_Lab(L, a, b, ill.name)

def Lab_to_XYZ(val:CIE_Lab) -> CIE_XYZ:
    ill = val.ill
    if not isinstance(ill, Illuminant):
        ill = get_illuminant(ill)
    
    def eps_func(num:float) -> float:
        if num**3 > CIE_CORRECTED_EPSILON:
            return num ** 3
        return (116*num - 16)/CIE_CORRECTED_KAPPA

    fy = (val.L + 16)/116
    yr = val.L / CIE_CORRECTED_KAPPA
    if val.L > CIE_CORRECTED_EPSILON*CIE_CORRECTED_KAPPA:
        yr = fy ** 3

    fx = (val.a/500) + fy
    fz = fy - (val.b/200)
    xr, zr = eps_func(fx), eps_func(fz) 

    x = xr * ill.X
    y = yr * ill.Y
    z = zr * ill.Z

    return CIE_XYZ(x, y, z)

def Lab_to_LCHab(val:CIE_Lab) -> LCHab:
    tmp = np.rad2deg(np.atan2(val.b, val.a))
    C = np.sqrt(val.a**2 + val.b**2)
    H = tmp if tmp else 360
    return LCHab(val.L, C, H, val.ill)

def LCHab_to_Lab(val:LCHab) -> CIE_Lab:
    a = val.C*np.cos(np.deg2rad(val.H))
    b = val.C*np.sin(np.deg2rad(val.H))
    return CIE_Lab(val.L, a, b, val.ill)

def XYZ_to_xyY(val:CIE_XYZ) -> CIE_xyY:
    denom = val.to_numpy().sum() if val.to_numpy().sum() else 1.
    x = val.x / denom
    y = val.y / denom
    return CIE_xyY(x, y, val.y)

def xyY_to_XYZ(val:CIE_xyY):
    if val.y == 0:
        return CIE_XYZ(0,0,0)

    x = (val.Y*val.x)/val.y
    y = val.Y
    z = (val.Y*val.z())/val.y
    return CIE_XYZ(x, y, z)

def XYZ_to_RGB(val:CIE_XYZ, space:Literal[RGB_WORKING_SPACE]="CIE_RGB") -> RGB:
    space = get_working_space(space)
    rgb = (val.to_numpy() @ space.M_inv).tolist()
    return RGB(rgb[0], rgb[1], rgb[2])

def RGB_to_XYZ(val:RGB, space:Literal[RGB_WORKING_SPACE]="CIE_RGB") -> CIE_XYZ:
    space = get_working_space(space)
    XYZ = (val.to_numpy() @ space.M).tolist()
    return CIE_XYZ(XYZ[0], XYZ[1], XYZ[2])


