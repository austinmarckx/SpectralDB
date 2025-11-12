import numpy as np
from typing import Literal, Optional, Any, NamedTuple, Union, Callable

type Element = Literal["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr", "Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr"]
type StandardIlluminant = Literal["D65", "E"]
type RGBTuple = tuple[float, float, float]
type RGBATuple = tuple[float, float, float, float]

class CIE_XYZ(NamedTuple):
    """ """
    x:float
    y:float
    z:float
    deg:Literal[2, 10, 1931, 1964, 1965]

class sRGB(NamedTuple):
    r:float
    g:float
    b:float

class Color(NamedTuple):
    rgb:tuple[float,float,float]

class Illuminant(NamedTuple):
    """ 
    Theoretically you can construct an illumnant
    I'd like to do that in the future, but not sure how yet. 
    this is a placeholder for now.
    """
    pass

class Wavelength(NamedTuple):
    wl:float
    srgb:Optional[sRGB]=None
    xyz:Optional[CIE_XYZ]=None
    illuminant:Optional[Union[Illuminant,StandardIlluminant]]=None
    
class ColorRange(NamedTuple):
    lower:float
    upper:float
    r:int
    g:int
    b:int
    a:float=1.0

    def to_colorscale(self):
        return [
            (self.lower, f"rgba({self.r}, {self.g}, {self.b}, {self.a})"),
            (self.upper, f"rgba({self.r}, {self.g}, {self.b}, {self.a})"),
        ]



class InvalidElementError(Exception):
    pass

class TestInputs(NamedTuple):
    args:Optional[tuple]=None
    kwargs:Optional[dict]=None

    def to_params(self) -> tuple[tuple,dict]:
        args = self.args if self.args is not None else tuple()
        kwargs = self.kwargs if self.kwargs is not None else {}
        return args, kwargs

class TestOutputs(NamedTuple):
    outputs:Optional[Any]=None

class TestTuple(NamedTuple):
    name:str
    inputs:TestInputs
    outputs:TestOutputs
    func:Callable

    @classmethod
    def make(cls, cond:dict) -> 'TestTuple':
        return TestTuple(cond.get("name"), TestInputs(**cond.get("inputs", {})), TestOutputs(cond.get("outputs", {})), cond.get("func", None))

    def i(self):
        return self.inputs
    
    def o(self):
        return self.outputs