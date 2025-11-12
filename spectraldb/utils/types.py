import numpy as np
from typing import Literal, Optional, Any, NamedTuple, Union, Callable

# plotly.express.colors.named_colorscales()
PLOTLY_COLORSCALES = ['aggrnyl', 'agsunset', 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'darkmint', 'electric', 'emrld', 'gnbu', 'greens', 'greys', 'hot', 'inferno', 'jet', 'magenta', 'magma', 'mint', 'orrd', 'oranges', 'oryel', 'peach', 'pinkyl', 'plasma', 'plotly3', 'pubu', 'pubugn', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdpu', 'redor', 'reds', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'turbo', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd', 'algae', 'amp', 'deep', 'dense', 'gray', 'haline', 'ice', 'matter', 'solar', 'speed', 'tempo', 'thermal', 'turbid', 'armyrose', 'brbg', 'earth', 'fall', 'geyser', 'prgn', 'piyg', 'picnic', 'portland', 'puor', 'rdgy', 'rdylbu', 'rdylgn', 'spectral', 'tealrose', 'temps', 'tropic', 'balance', 'curl', 'delta', 'oxy', 'edge', 'hsv', 'icefire', 'phase', 'twilight', 'mrybm','mygbm']
PLOTLY_REVERSE_COLORSCALES = ['aggrnyl_r', 'agsunset_r', 'blackbody_r', 'bluered_r', 'blues_r', 'blugrn_r', 'bluyl_r', 'brwnyl_r', 'bugn_r', 'bupu_r', 'burg_r', 'burgyl_r', 'cividis_r', 'darkmint_r', 'electric_r', 'emrld_r', 'gnbu_r', 'greens_r', 'greys_r', 'hot_r', 'inferno_r', 'jet_r', 'magenta_r', 'magma_r', 'mint_r', 'orrd_r', 'oranges_r', 'oryel_r', 'peach_r', 'pinkyl_r', 'plasma_r', 'plotly3_r', 'pubu_r', 'pubugn_r', 'purd_r', 'purp_r', 'purples_r', 'purpor_r', 'rainbow_r', 'rdbu_r', 'rdpu_r', 'redor_r', 'reds_r', 'sunset_r', 'sunsetdark_r', 'teal_r', 'tealgrn_r', 'turbo_r', 'viridis_r', 'ylgn_r', 'ylgnbu_r', 'ylorbr_r', 'ylorrd_r', 'algae_r', 'amp_r', 'deep_r', 'dense_r', 'gray_r', 'haline_r', 'ice_r', 'matter_r', 'solar_r', 'speed_r', 'tempo_r', 'thermal_r', 'turbid_r', 'armyrose_r', 'brbg_r', 'earth_r', 'fall_r', 'geyser_r', 'prgn_r', 'piyg_r', 'picnic_r', 'portland_r', 'puor_r', 'rdgy_r', 'rdylbu_r', 'rdylgn_r', 'spectral_r', 'tealrose_r', 'temps_r', 'tropic_r', 'balance_r', 'curl_r', 'delta_r', 'oxy_r', 'edge_r', 'hsv_r', 'icefire_r', 'phase_r', 'twilight_r', 'mrybm_r', 'mygbm_r']

type CustomColorscale = list[ColorRange]
type PlotlyColorscale =  Literal['aggrnyl', 'agsunset', 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'darkmint', 'electric', 'emrld', 'gnbu', 'greens', 'greys', 'hot', 'inferno', 'jet', 'magenta', 'magma', 'mint', 'orrd', 'oranges', 'oryel', 'peach', 'pinkyl', 'plasma', 'plotly3', 'pubu', 'pubugn', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdpu', 'redor', 'reds', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'turbo', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd', 'algae', 'amp', 'deep', 'dense', 'gray', 'haline', 'ice', 'matter', 'solar', 'speed', 'tempo', 'thermal', 'turbid', 'armyrose', 'brbg', 'earth', 'fall', 'geyser', 'prgn', 'piyg', 'picnic', 'portland', 'puor', 'rdgy', 'rdylbu', 'rdylgn', 'spectral', 'tealrose', 'temps', 'tropic', 'balance', 'curl', 'delta', 'oxy', 'edge', 'hsv', 'icefire', 'phase', 'twilight', 'mrybm','mygbm', 'aggrnyl_r', 'agsunset_r', 'blackbody_r', 'bluered_r', 'blues_r', 'blugrn_r', 'bluyl_r', 'brwnyl_r', 'bugn_r', 'bupu_r', 'burg_r', 'burgyl_r', 'cividis_r', 'darkmint_r', 'electric_r', 'emrld_r', 'gnbu_r', 'greens_r', 'greys_r', 'hot_r', 'inferno_r', 'jet_r', 'magenta_r', 'magma_r', 'mint_r', 'orrd_r', 'oranges_r', 'oryel_r', 'peach_r', 'pinkyl_r', 'plasma_r', 'plotly3_r', 'pubu_r', 'pubugn_r', 'purd_r', 'purp_r', 'purples_r', 'purpor_r', 'rainbow_r', 'rdbu_r', 'rdpu_r', 'redor_r', 'reds_r', 'sunset_r', 'sunsetdark_r', 'teal_r', 'tealgrn_r', 'turbo_r', 'viridis_r', 'ylgn_r', 'ylgnbu_r', 'ylorbr_r', 'ylorrd_r', 'algae_r', 'amp_r', 'deep_r', 'dense_r', 'gray_r', 'haline_r', 'ice_r', 'matter_r', 'solar_r', 'speed_r', 'tempo_r', 'thermal_r', 'turbid_r', 'armyrose_r', 'brbg_r', 'earth_r', 'fall_r', 'geyser_r', 'prgn_r', 'piyg_r', 'picnic_r', 'portland_r', 'puor_r', 'rdgy_r', 'rdylbu_r', 'rdylgn_r', 'spectral_r', 'tealrose_r', 'temps_r', 'tropic_r', 'balance_r', 'curl_r', 'delta_r', 'oxy_r', 'edge_r', 'hsv_r', 'icefire_r', 'phase_r', 'twilight_r', 'mrybm_r', 'mygbm_r']
type Colorscale = Union[PlotlyColorscale, CustomColorscale]
type Element = Literal["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr", "Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr"]
type CIEReference = Literal["1931_deg2", "2006_deg2", "2006_deg10"]
type StandardIlluminant = Literal["D65", "E"]
type RGBTuple = tuple[float, float, float]
type RGBATuple = tuple[float, float, float, float]

class CIE_XYZ(NamedTuple):
    """ """
    x:float
    y:float
    z:float
    deg:Optional[Literal["2", "10", "1931", "1964", "1965"]]=None

class sRGB(NamedTuple):
    r:float
    g:float
    b:float

class Color(NamedTuple):
    rgb:RGBTuple

    def tostr(self):
        return f"rgb({self.rgb[0]},{self.rgb[1]},{self.rgb[2]})"

    def tohex(self):
        return "#%x%x%x"%self.rgb

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