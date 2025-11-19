""" Working space matrix conversions (credit to: Bruce Lindbloom)
retrieved from http://brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
http://www.brucelindbloom.com/index.html



"""
import numpy as np
from spectraldb.utils.types import WorkingSpace, NamedWorkingSpace, CIE_xyY, NamedIlluminant, Illuminant
from spectraldb.illuminant import get_illuminant

Adobe_RGB_1998 = {
    "name":"Adobe_RGB_1998",
    "ill":"D65",
    "M": np.array([
        [0.5767309,  0.1855540,  0.1881852],
        [0.2973769,  0.6273491,  0.0752741],
        [0.0270343,  0.0706872,  0.9911085],
    ]),
    "M_inv": np.array([
        [2.0413690, -0.5649464, -0.3446944],
        [-0.9692660,  1.8760108,  0.0415560],
        [0.0134474, -0.1183897,  1.0154096],
    ]),
    "r_xyY":CIE_xyY(x=0.6400, y=0.3300, Y=0.297361),
    "g_xyY":CIE_xyY(x=0.2100, y=0.7100, Y=0.627355),
    "b_xyY":CIE_xyY(x=0.1500, y=0.0600, Y=0.075285),
    "gamma":2.2,
}
AppleRGB = {
    "name":"AppleRGB",
    "ill":"D65",
    "M": np.array([
        [ 0.4497288,  0.3162486,  0.1844926],
        [ 0.2446525,  0.6720283,  0.0833192],
        [ 0.0251848,  0.1411824,  0.9224628],
    ]),
    "M_inv": np.array([
        [ 2.9515373, -1.2894116, -0.4738445],
        [-1.0851093,  1.9908566,  0.0372026],
        [ 0.0854934, -0.2694964,  1.0912975],
    ]),
    "r_xyY":CIE_xyY(x=0.6250, y=0.3400, Y=0.244634),
    "g_xyY":CIE_xyY(x=0.2800, y=0.5950, Y=0.672034),
    "b_xyY":CIE_xyY(x=0.1550, y=0.0700, Y=0.083332),
    "gamma":1.8,
}
Best_RGB = {
    "name":"Best_RGB",
    "ill":"D50",
    "M": np.array([
        [ 0.6326696,  0.2045558,  0.1269946],
        [ 0.2284569,  0.7373523,  0.0341908],
        [ 0.0000000,  0.0095142,  0.8156958],
    ]),
    "M_inv": np.array([
        [ 1.7552599, -0.4836786, -0.2530000],
        [-0.5441336,  1.5068789,  0.0215528],
        [ 0.0063467, -0.0175761,  1.2256959],
    ]),
    "r_xyY":CIE_xyY(x=0.7347, y=0.2653, Y=0.228457),
    "g_xyY":CIE_xyY(x=0.2150, y=0.7750, Y=0.737352),
    "b_xyY":CIE_xyY(x=0.1300, y=0.0350, Y=0.034191),
    "gamma":2.2,
}
Beta_RGB = {								
    "name":"Beta_RGB",
    "ill":"D50",
    "M": np.array([
        [ 0.6712537,  0.1745834,  0.1183829],
        [ 0.3032726,  0.6637861,  0.0329413],
        [ 0.0000000,  0.0407010,  0.7845090],
    ]),
    "M_inv": np.array([
        [ 1.6832270, -0.4282363, -0.2360185],
        [-0.7710229,  1.7065571,  0.0446900],
        [ 0.0400013, -0.0885376,  1.2723640],
    ]),
    "r_xyY":CIE_xyY(x=0.6888, y=0.3112, Y=0.303273),
    "g_xyY":CIE_xyY(x=0.1986, y=0.7551, Y=0.663786),
    "b_xyY":CIE_xyY(x=0.1265, y=0.0352, Y=0.032941),
    "gamma":2.2,
}
Bruce_RGB = {								
    "name":"Bruce_RGB",
    "ill":"D65",
    "M": np.array([
        [ 0.4674162,  0.2944512,  0.1886026],
        [ 0.2410115,  0.6835475,  0.0754410],
        [ 0.0219101,  0.0736128,  0.9933071],
    ]),
    "M_inv": np.array([
        [ 2.7454669, -1.1358136, -0.4350269],
        [-0.9692660,  1.8760108,  0.0415560],
        [ 0.0112723, -0.1139754,  1.0132541],
    ]),
    "r_xyY":CIE_xyY(x=0.6400, y=0.3300, Y=0.240995),
    "g_xyY":CIE_xyY(x=0.2800, y=0.6500, Y=0.683554),
    "b_xyY":CIE_xyY(x=0.1500, y=0.0600, Y=0.075452),
    "gamma":2.2,
}
CIE_RGB = {
    "name":"CIE_RGB",
    "ill":"E",
    "M": np.array([
        [ 0.4887180,  0.3106803,  0.2006017],
        [ 0.1762044,  0.8129847,  0.0108109],
        [ 0.0000000,  0.0102048,  0.9897952],
    ]),
    "M_inv": np.array([
        [ 2.3706743, -0.9000405, -0.4706338],
        [-0.5138850,  1.4253036,  0.0885814],
        [ 0.0052982, -0.0146949,  1.0093968],
    ]),
    "r_xyY":CIE_xyY(x=0.7350, y=0.2650, Y=0.176204),
    "g_xyY":CIE_xyY(x=0.2740, y=0.7170, Y=0.812985),
    "b_xyY":CIE_xyY(x=0.1670, y=0.0090, Y=0.010811),
    "gamma":2.2,
}
ColorMatch_RGB = {
    "name":"ColorMatch_RGB",
    "ill":"D50",
    "M": np.array([
        [ 0.5093439,  0.3209071,  0.1339691],
        [ 0.2748840,  0.6581315,  0.0669845],
        [ 0.0242545,  0.1087821,  0.6921735],
    ]),
    "M_inv": np.array([
        [ 2.6422874, -1.2234270, -0.3930143],
        [-1.1119763,  2.0590183,  0.0159614],
        [ 0.0821699, -0.2807254,  1.4559877],
    ]),
    "r_xyY":CIE_xyY(x=0.6300, y=0.3400, Y=0.274884),
    "g_xyY":CIE_xyY(x=0.2950, y=0.6050, Y=0.658132),
    "b_xyY":CIE_xyY(x=0.1500, y=0.0750, Y=0.066985),
    "gamma":1.8,
}									
Don_RGB_4 = {
    "name":"Don_RGB_4",
    "ill":"D50",
    "M": np.array([
        [ 0.6457711,  0.1933511,  0.1250978],
        [ 0.2783496,  0.6879702,  0.0336802],
        [ 0.0037113,  0.0179861,  0.8035125],
    ]),
    "M_inv": np.array([
        [ 1.7603902, -0.4881198, -0.2536126],
        [-0.7126288,  1.6527432,  0.0416715],
        [ 0.0078207, -0.0347411,  1.2447743],
    ]),
    "r_xyY":CIE_xyY(x=0.6960, y=0.3000, Y=0.278350),
    "g_xyY":CIE_xyY(x=0.2150, y=0.7650, Y=0.687970),
    "b_xyY":CIE_xyY(x=0.1300, y=0.0350, Y=0.033680),
    "gamma":2.2,
} 								
ECI_RGB = {
    "name":"ECI_RGB",
    "ill":"D50",
    "M": np.array([
        [ 0.6502043,  0.1780774,  0.1359384],
        [ 0.3202499,  0.6020711,  0.0776791],
        [ 0.0000000,  0.0678390,  0.7573710],
    ]),
    "M_inv": np.array([
        [ 1.7827618, -0.4969847, -0.2690101],
        [-0.9593623,  1.9477962, -0.0275807],
        [ 0.0859317, -0.1744674,  1.3228273],
    ]),
    "r_xyY":CIE_xyY(x=0.6700, y=0.3300, Y=0.320250),
    "g_xyY":CIE_xyY(x=0.2100, y=0.7100, Y=0.602071),
    "b_xyY":CIE_xyY(x=0.1400, y=0.0800, Y=0.077679),
}								
Ekta_Space_PS5 = {
    "name":"Ekta_Space_PS5",
    "ill":"D50",
    "M": np.array([
        [ 0.5938914,  0.2729801,  0.0973485],
        [ 0.2606286,  0.7349465,  0.0044249],
        [ 0.0000000,  0.0419969,  0.7832131],
    ]),
    "M_inv": np.array([
        [ 2.0043819, -0.7304844, -0.2450052],
        [-0.7110285,  1.6202126,  0.0792227],
        [ 0.0381263, -0.0868780,  1.2725438],
    ]),
    "r_xyY":CIE_xyY(x=0.6950, y=0.3050, Y=0.260629),
    "g_xyY":CIE_xyY(x=0.2600, y=0.7000, Y=0.734946),
    "b_xyY":CIE_xyY(x=0.1100, y=0.0050, Y=0.004425),
    "gamma":2.2,
}								
NTSC_RGB = {
    "name":"NTSC_RGB",
    "ill":"C",
    "M": np.array([
        [ 0.6068909,  0.1735011,  0.2003480],
        [ 0.2989164,  0.5865990,  0.1144845],
        [ 0.0000000,  0.0660957,  1.1162243],
    ]),
    "M_inv": np.array([
        [ 1.9099961, -0.5324542, -0.2882091],
        [-0.9846663,  1.9991710, -0.0283082],
        [ 0.0583056, -0.1183781,  0.8975535],
    ]),
    "r_xyY":CIE_xyY(x=0.6700, y=0.3300, Y=0.298839),
    "g_xyY":CIE_xyY(x=0.2100, y=0.7100, Y=0.586811),
    "b_xyY":CIE_xyY(x=0.1400, y=0.0800, Y=0.114350),
    "gamma":2.2,
} 								
PAL_SECAM_RGB = {
    "name":"PAL_SECAM_RGB",
    "ill":"D65",
    "M": np.array([
        [ 0.4306190,  0.3415419,  0.1783091],
        [ 0.2220379,  0.7066384,  0.0713236],
        [ 0.0201853,  0.1295504,  0.9390944],
    ]),
    "M_inv": np.array([
        [ 3.0628971, -1.3931791, -0.4757517],
        [-0.9692660,  1.8760108,  0.0415560],
        [ 0.0678775, -0.2288548,  1.0693490],
    ]),
    "r_xyY":CIE_xyY(x=0.6400, y=0.3300, Y=0.222021),
    "g_xyY":CIE_xyY(x=0.2900, y=0.6000, Y=0.706645),
    "b_xyY":CIE_xyY(x=0.1500, y=0.0600, Y=0.071334),
    "gamma":2.2,
} 								
ProPhoto_RGB = {
    "name":"ProPhoto_RGB",
    "ill":"D50",
    "M": np.array([
        [ 0.7976749,  0.1351917,  0.0313534],
        [ 0.2880402,  0.7118741,  0.0000857],
        [ 0.0000000,  0.0000000,  0.8252100],
    ]),
    "M_inv": np.array([
        [ 1.3459433, -0.2556075, -0.0511118],
        [-0.5445989,  1.5081673,  0.0205351],
        [ 0.0000000,  0.0000000,  1.2118128],
    ]),
    "r_xyY":CIE_xyY(x=0.7347, y=0.2653, Y=0.288040),
    "g_xyY":CIE_xyY(x=0.1596, y=0.8404, Y=0.711874),
    "b_xyY":CIE_xyY(x=0.0366, y=0.0001, Y=0.000086),
    "gamma":1.8,
}						
SMPTE_C_RGB = {
    "name":"SMPTE_C_RGB",
    "ill":"D65",
    "M": np.array([
        [ 0.3935891,  0.3652497,  0.1916313],
        [ 0.2124132,  0.7010437,  0.0865432],
        [ 0.0187423,  0.1119313,  0.9581563],
    ]),
    "M_inv": np.array([
        [ 3.5053960, -1.7394894, -0.5439640],
        [-1.0690722,  1.9778245,  0.0351722],
        [ 0.0563200, -0.1970226,  1.0502026],
    ]),
    "r_xyY":CIE_xyY(x=0.6300, y=0.3400, Y=0.212395),
    "g_xyY":CIE_xyY(x=0.3100, y=0.5950, Y=0.701049),
    "b_xyY":CIE_xyY(x=0.1550, y=0.0700, Y=0.086556),
    "gamma":2.2,
} 								
sRGB = {
    "name":"sRGB",
    "ill":"D65",
    "M": np.array([
        [ 0.4124564,  0.3575761,  0.1804375],
        [ 0.2126729,  0.7151522,  0.0721750],
        [ 0.0193339,  0.1191920,  0.9503041],
    ]),
    "M_inv": np.array([
        [ 3.2404542, -1.5371385, -0.4985314],
        [-0.9692660,  1.8760108,  0.0415560],
        [ 0.0556434, -0.2040259,  1.0572252],
    ]),
    "r_xyY":CIE_xyY(x=0.6400, y=0.3300, Y=0.212656),
    "g_xyY":CIE_xyY(x=0.3000, y=0.6000, Y=0.715158),
    "b_xyY":CIE_xyY(x=0.1500, y=0.0600, Y=0.072186),
    "gamma":2.2,
}	
Wide_Gamut_RGB = {
    "name":"Wide_Gamut_RGB",
    "ill":"D50",
    "M": np.array([
        [ 0.7161046,  0.1009296,  0.1471858],
        [ 0.2581874,  0.7249378,  0.0168748],
        [ 0.0000000,  0.0517813,  0.7734287],
    ]),
    "M_inv": np.array([
        [ 1.4628067, -0.1840623, -0.2743606],
        [-0.5217933,  1.4472381,  0.0677227],
        [ 0.0349342, -0.0968930,  1.2884099],
    ]),
    "r_xyY":CIE_xyY(x=0.7350, y=0.2650, Y=0.258187),
    "g_xyY":CIE_xyY(x=0.1150, y=0.8260, Y=0.724938),
    "b_xyY":CIE_xyY(x=0.1570, y=0.0180, Y=0.016875),
    "gamma":2.2,
} 								

WORKING_SPACES_LIST = [
    Adobe_RGB_1998, AppleRGB, Best_RGB, Beta_RGB, Bruce_RGB, CIE_RGB, ColorMatch_RGB, 
    Don_RGB_4, ECI_RGB, Ekta_Space_PS5, NTSC_RGB, PAL_SECAM_RGB, ProPhoto_RGB, SMPTE_C_RGB, 
    sRGB, Wide_Gamut_RGB
]
WORKING_SPACES_DICT = {ws["name"]:WorkingSpace(**ws) for ws in WORKING_SPACES_LIST}


def create_working_space(name:str, red:CIE_xyY, green:CIE_xyY, blue:CIE_xyY, ill:NamedIlluminant):
    if not isinstance(ill, Illuminant):
        ill = get_illuminant(ill)
    
    def _xyY_to_XYZ(xyY:CIE_xyY) -> tuple[float, float, float]:
        if xyY.y == 0:
            return 0, 0, 0
        x = (xyY.Y*xyY.x)/xyY.y
        y = xyY.Y
        z = (xyY.Y*xyY.z())/xyY.y
        return x, y, z
    
    xr, yr, zr = _xyY_to_XYZ(red)
    xg, yg, zg = _xyY_to_XYZ(green)
    xb, yb, zb = _xyY_to_XYZ(blue)

    mat = np.array([
        [xr, xg, xb],
        [yr, yg, yb],
        [zr, zg, zb],
    ])

    S = np.linalg.inv(mat) @ ill.to_numpy()
    sr, sg, sb = S[0], S[1], S[2]

    M = np.array([
        [sr*xr, sg*xg, sb*xb],
        [sr*yr, sg*yg, sb*yb],
        [sr*zr, sg*zg, sb*zb],
    ])
    M_inv = np.linalg.inv(M)

    return WorkingSpace(name=name, ill=ill.name, M=M, M_inv=M_inv, r_xyY=red, g_xyY=green, b_xyY=blue)
    


def get_working_space(ws:NamedWorkingSpace) -> WorkingSpace:
    try:
        return WORKING_SPACES_DICT[ws]
    except:
        raise ValueError(f"{ws} is not a recognized working space")


