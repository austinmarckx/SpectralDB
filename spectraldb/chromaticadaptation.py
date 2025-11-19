import numpy as np
from typing import Literal, Union
from spectraldb.utils.types import ChromaticAdaptation, NamedIlluminant, CIE_XYZ
from spectraldb.illuminant import get_illuminant

XYZ_Scaling = {
    "name":"XYZ_Scaling",
    "M": np.array([
        [ 1.0000000,  0.0000000,  0.0000000],
        [ 0.0000000,  1.0000000,  0.0000000],
        [ 0.0000000,  0.0000000,  1.0000000],
    ]),
    "M_inv": np.array([
        [ 1.0000000,  0.0000000,  0.0000000],
        [ 0.0000000,  1.0000000,  0.0000000],
        [ 0.0000000,  0.0000000,  1.0000000],
    ]),
}
Bradford = {
    "name":"Bradford",
    "M": np.array([
        [ 0.8951000,  0.2664000, -0.1614000],
        [-0.7502000,  1.7135000,  0.0367000],
        [ 0.0389000, -0.0685000,  1.0296000],
    ]),
    "M_inv": np.array([
        [ 0.9869929, -0.1470543,  0.1599627],
        [ 0.4323053,  0.5183603,  0.0492912],
        [-0.0085287,  0.0400428,  0.9684867],
    ]),
}
VonKries = {
    "name":"VonKries",
    "M": np.array([
        [ 0.4002400,  0.7076000, -0.0808100],
        [-0.2263000,  1.1653200,  0.0457000],
        [ 0.0000000,  0.0000000,  0.9182200],
    ]),
    "M_inv": np.array([
        [ 1.8599364, -1.1293816,  0.2198974],
        [ 0.3611914,  0.6388125, -0.0000064],
        [ 0.0000000,  0.0000000,  1.0890636],
    ]),
}

ADAPTATION_DICT = {
    "xyz_scaling":ChromaticAdaptation(**XYZ_Scaling),
    "bradford":ChromaticAdaptation(**Bradford),
    "vonkries":ChromaticAdaptation(**VonKries),
}
type Adaptation = Literal["xyz_scaling", "bradford", "vonkries"]

def get_adaptation(adapt:Adaptation):
    try:
        return ADAPTATION_DICT[adapt]
    except:
        raise ValueError(f"{adapt} is not a recognized chromatic adaptation")
    
def adaptation_matrix(src_ill:NamedIlluminant, dest_ill:NamedIlluminant, adaptation:Union[Adaptation, ChromaticAdaptation]="xyz_scaling") -> np.ndarray:
    if isinstance(adaptation, str):
        A = get_adaptation(adaptation)    
    if isinstance(src_ill, str):
        src_ill = get_illuminant(src_ill)
    if isinstance(dest_ill, str):
        dest_ill = get_illuminant(dest_ill)

    src_ill_cone_resp = A.M @ src_ill.to_numpy()
    dest_ill_cone_resp = A.M @ dest_ill.to_numpy()
    ratios = np.identity(3) * (dest_ill_cone_resp / src_ill_cone_resp)
    M = A.M_inv @ ratios @ A.M
    return M

def adapt(source:CIE_XYZ, dest_ill:NamedIlluminant,  adaptation:Union[Adaptation, ChromaticAdaptation]="xyz_scaling", src_ill:NamedIlluminant="E",) -> CIE_XYZ:
    M = adaptation_matrix(src_ill, dest_ill, adaptation)
    dest = M @ source.to_numpy()
    return CIE_XYZ(x=dest[0], y=dest[1], z=dest[2], deg=source.deg)
