from typing import Literal, Optional, Any, NamedTuple

type Element = Literal["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr", "Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr"]


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

    @classmethod
    def make(cls, cond:dict) -> 'TestTuple':
        return TestTuple(cond.get("name"), TestInputs(**cond.get("inputs", {})), TestOutputs(cond.get("outputs", {})))

    def i(self):
        return self.inputs
    
    def o(self):
        return self.outputs