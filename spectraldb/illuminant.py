from spectraldb.utils.types import Illuminant, StandardIlluminant, InvalidIlluminantError

illuminantA = Illuminant("A", X=1.09850, Y=1.00000, Z=0.35585)
illuminantB = Illuminant("B", X=0.99072, Y=1.00000, Z=0.85223)
illuminantC = Illuminant("C", X=0.98074, Y=1.00000, Z=1.18232)
illuminantD50 = Illuminant("D50", X=0.96422, Y=1.00000, Z=0.82521)
illuminantD55 = Illuminant("D55", X=0.95682, Y=1.00000, Z=0.92149)
illuminantD65 = Illuminant("D65", X=0.95047, Y=1.00000, Z=1.08883)
illuminantD75 = Illuminant("D65", X=0.94972, Y=1.00000, Z=1.22638)
illuminantE = Illuminant("E", X=1.00000, Y=1.00000, Z=1.00000)
illuminantF2 = Illuminant("F2", X=0.99186, Y=1.00000, Z=0.67393)
illuminantF7 = Illuminant("F7", X=0.95041, Y=1.00000, Z=1.08747)
illuminantF11 = Illuminant("F11", X=1.00962, Y=1.00000, Z=0.64350)

ILLUMINANT_DICT = {
    "A": illuminantA,
    "B": illuminantB,
    "C": illuminantC, 
    "D50":illuminantD50, 
    "D55":illuminantD55, 
    "D65":illuminantD65,
    "D75":illuminantD75,
    "E": illuminantE,
    "F2": illuminantF2,
    "F7": illuminantF7,
    "F11": illuminantF11,
}

def get_illuminant(ill:StandardIlluminant) -> Illuminant:
    try:
        return ILLUMINANT_DICT[ill]
    except:
        raise InvalidIlluminantError(f"{ill} is not a recognized illuminant")