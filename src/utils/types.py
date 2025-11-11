import numpy as np
from typing import Literal, Optional, Any, NamedTuple, Union, Callable

type Element = Literal["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr", "Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr"]
type StandardIlluminant = Literal["D65", "E"]

class CIE_XYZ(NamedTuple):
    """ """
    x:float
    y:float
    z:float
    deg:Literal[2, 10, 1931, 1964, 1965]

    def as_RGB(self) -> 'RGB':
        M_inv = np.matrix([
            [2.3644, -0.8958, -0.4686],
            [-0.5148, 1.4252, 0.0896],
            [0.0052, -0.0144, 1.0092],
        ])
        rgb = np.arr([self.x, self.y, self.z]) @ M_inv
        return RGB(rgb[0], rgb[1], rgb[2])

class RGB(NamedTuple):
    r:float
    g:float
    b:float
    
    def as_XYZ(self) -> CIE_XYZ:
        M = np.matrix([
            [0.490, 0.310, 0.200],
            [0.177, 0.813, 0.010],
            [0.000, 0.010, 0.990],
        ])
        XYZ = np.arr([self.r, self.g, self.b]) @ M
        return CIE_XYZ(XYZ[0], XYZ[1], XYZ[2], 2)


class Illuminant(NamedTuple):
    """ 
    Theoretically you can construct an illumnant
    I'd like to do that in the future, but not sure how yet. 
    this is a placeholder for now.
    """
    pass

class Wavelength(NamedTuple):
    wl:float
    rgb:Optional[RGB]=None
    xyz:Optional[CIE_XYZ]=None
    illuminant:Optional[Union[Illuminant,StandardIlluminant]]=None
    
    



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