import numpy as np
from spectraldb.utils.types import CIE_XYZ, sRGB, Color

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
    return CIE_XYZ(XYZ[0][0], XYZ[0][1], XYZ[0][2], 2)