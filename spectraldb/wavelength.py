
import random
import pandas as pd
from spectraldb.utils.types import RGB, CIE_Lab, CIE_xyY, CIE_XYZ, LCHab, LCHuv, Luv, NamedIlluminant, NamedWorkingSpace
from typing import Optional, Self, NamedTuple, Union
from spectraldb.colorspaces import wavelength_to_XYZ, XYZ_to_xyY, XYZ_to_Lab, XYZ_to_Luv, XYZ_to_RGB, Luv_to_LCHuv, Lab_to_LCHab, wein_approx


class Wavelength:
    
    def __init__(self,
        wl:float,
        xyz:Optional[CIE_XYZ]=None,
        xyY:Optional[CIE_xyY]=None,
        lab:Optional[CIE_Lab]=None,
        lchab:Optional[LCHab]=None,
        luv:Optional[Luv]=None,
        lchuv:Optional[LCHuv]=None,
        cct:Optional[float]=None,
        rgb:Optional[RGB]=None,
        space:Optional[NamedWorkingSpace]="CIE_RGB",
        illuminant:Optional[NamedIlluminant]="E",
        ) -> None:
        self.wl = wl
        self.xyz = xyz
        self.xyY = xyY
        self.lab = lab
        self.lchab = lchab
        self.luv = luv
        self.lchuv = lchuv
        self.cct = cct
        self.rgb = rgb
        self.space = space
        self.ill = illuminant
        
        self.make()
    
    def make(self):
        if self.xyz is None:
            self.xyz = wavelength_to_XYZ(self.wl)
        if self.xyY is None:
            self.xyY = XYZ_to_xyY(self.xyz)
        if self.lab is None:
            self.lab = XYZ_to_Lab(self.xyz, self.ill)
        if self.lchab is None:
            self.lchab = Lab_to_LCHab(self.lab)
        if self.luv is None:
            self.luv = XYZ_to_Luv(self.xyz, self.ill)
        if self.lchuv is None:
            self.lchuv = Luv_to_LCHuv(self.luv)
        if self.cct is None:
            self.cct = wein_approx(self.wl)
        if self.rgb is None:
            self.rgb = XYZ_to_RGB(self.xyz, self.space)
 
    

def select_random_wavelengths(df:pd.DataFrame, n:int=1, col:str="wavelength_nm") -> Union[list[Wavelength], Wavelength]:
    chosen = random.sample(df[col].to_list(), n)
    waves = [Wavelength(c) for c in chosen]
    if len(waves) > 1:
        return waves
    return waves[0]