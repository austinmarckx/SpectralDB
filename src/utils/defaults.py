import os

SPECTRALDB_ABS_PATH = os.path.sep.join(os.path.abspath("defaults.py").split(os.path.sep)[:-2])
RAW_LINES_PATH = os.path.sep.join([SPECTRALDB_ABS_PATH,"data", "raw", "lines","wavelength"])

UNITTEST_SETUP_STRING = """\n .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .-----------------. .----------------.   
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |  
| |  _________   | || |  _________   | || |    _______   | || |  _________   | || |     _____    | || | ____  _____  | || |    ______    | |  
| | |  _   _  |  | || | |_   ___  |  | || |   /  ___  |  | || | |  _   _  |  | || |    |_   _|   | || ||_   \|_   _| | || |  .' ___  |   | |  
| | |_/ | | \_|  | || |   | |_  \_|  | || |  |  (__ \_|  | || | |_/ | | \_|  | || |      | |     | || |  |   \ | |   | || | / .'   \_|   | |  
| |     | |      | || |   |  _|  _   | || |   '.___`-.   | || |     | |      | || |      | |     | || |  | |\ \| |   | || | | |    ____  | |  
| |    _| |_     | || |  _| |___/ |  | || |  |`\____) |  | || |    _| |_     | || |     _| |_    | || | _| |_\   |_  | || | \ `.___]  _| | |  
| |   |_____|    | || | |_________|  | || |  |_______.'  | || |   |_____|    | || |    |_____|   | || ||_____|\____| | || |  `._____.'   | |  
| |              | || |              | || |              | || |              | || |              | || |              | || |              | |  
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |  
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
"""


ELEMENTS = {
    "H":"Hydrogen","He":"Helium",
    "Li":"Lithium","Be":"Beryllium","B":"Boron","C":"Carbon","N":"Nitrogen","O":"Oxygen","F":"Fluorine","Ne":"Neon",
    "Na":"Sodium","Mg":"Magnesium","Al":"Aluminium","Si":"Silicon","P":"Phosphorus","S":"Sulfur","Cl":"Chlorine","Ar":"Argon",
    "K":"Potassium","Ca":"Calcium","Sc":"Scandium","Ti":"Titanium","V":"Vandium","Cr":"Chromium","Mn":"Manganese","Fe":"Iron","Co":"Cobalt","Ni":"Nickel","Cu":"Copper","Zn":"Zinc","Ga":"Gallium","Ge":"Germanium","As":"Arsenic","Se":"Selenium","Br":"Bromine","Kr":"Krypton",
    "Rb":"Rubidium","Sr":"Strontium","Y":"Yttrium","Zr":"Zirconium","Nb":"Niobium","Mo":"Molybdenum","Tc":"Technetium","Ru":"Ruthenium","Rh":"Rhodium","Pd":"Palladium","Ag":"Silver","Cd":"Cadmium","In":"Indium","Sn":"Tin","Sb":"Antimony","Te":"Tellurium","I":"Iodine","Xe":"Xenon",
    "Cs":"Caesium","Ba":"Barium","La":"Lanthanum","Hf":"Hafnium","Ta":"Tantalum","W":"Tungsten","Re":"Rhenium","Os":"Osmium","Ir":"Iridium","Pt":"Platinum","Au":"Gold","Hg":"Mercury","Tl":"Thallium","Pb":"Lead","Bi":"Bismuth","Po":"Polonium","At":"Astatine","Rn":"Radon",
    "Fr":"Francium","Ra":"Radium","Ac":"Actinium","Rf":"Rutherfordium","Db":"Dubnium","Sg":"Seaborgium","Bh":"Bohrium","Hs":"Hassium","Mt":"Meitnerium","Ds":"Darmstadtium","Rg":"Roentgenium","Cn":"Copernicium",
    
    "Ce":"Cerium","Pr":"Praseodymium","Nd":"Neodymium","Pm":"Promethium","Sm":"Samarium","Eu":"Europium","Gd":"Gadolinium","Tb":"Terbium","Dy":"Dysprosium","Ho":"Holmium","Er":"Erbium","Tm":"Thulium","Yb":"Ytterbium","Lu":"Lutetium",
    "Th":"Thorium","Pa":"Protactinium","U":"Uranium","Np":"Neptunium","Pu":"Plutonium","Am":"Americium","Cm":"Curium","Bk":"Berkelium","Cf":"Californium","Es":"Einsteinium","Fm":"Fermium","Md":"Mendelevium","No":"Nobelium","Lr":"Lawrencium", 
}
ELEMENTS_R = {v:k for k,v in ELEMENTS.items()}