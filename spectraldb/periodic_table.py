import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import json
from functools import partial
from itertools import chain
from typing import Optional, Union, Callable, Literal
from spectraldb.utils.io import load_cie_reference, get_element_name
from spectraldb.utils.types import Element, CIEReference, Colorscale 
from spectraldb.utils.preprocess import preprocess, filter_visible
from spectraldb.utils.misc import uno_reverse
from spectraldb.colorspaces import make_colorscale, normalize_wavelength, XYZ_to_color
from spectraldb.utils.defaults import DEFAULT_PLOTLY_LAYOUT, PERIODIC_JSON_PATH


PERIODIC_TABLE_LAYOUT = {
    "font":{'family': "Times New Roman", "size": 24},
    "title":{"text": "Periodic Table of Elements"},
    "xaxis":{"zeroline":False,"showgrid":False,"showticklabels":False, "ticks":"" },
    "yaxis":{"zeroline":False,"showgrid":False,"showticklabels":False, "ticks":"" },
    "plot_bgcolor":'white',
}

repeat_el = lambda v: [v, v]
unpack_el_range = lambda mn, mx: list(chain.from_iterable( [repeat_el(v) for v in range(mn, mx+1)] ))

def make_periodic_table_Z(size:int=3):
    repeat_el = lambda v: [v]*size
    unpack_el = lambda mn, mx: list(chain.from_iterable( [repeat_el(v) for v in range(mn, mx+1)] ))
    xlen = (size * 18) + 1  
    return [ 
    *[[ *[1 for _ in range(size)], *[None for _ in range(xlen-(2*size) )], *[2 for _ in range(size)] ] for _ in range(size)],
    *[[ *unpack_el(3,4), *[None for _ in range(xlen-(8*size))], *unpack_el(5,10) ] for _ in range(size)],
    *[[ *unpack_el(11,12), *[None for _ in range(xlen-(8*size))], *unpack_el(13,18) ] for _ in range(size)],
    *[[ *unpack_el(19,21), None, *unpack_el(22, 36) ] for _ in range(size)],
    *[[ *unpack_el(37,39), None, *unpack_el(40, 54) ] for _ in range(size)],
    *[[ *unpack_el(55,57), None, *unpack_el(72, 86) ] for _ in range(size)],
    *[[ *unpack_el(87,89), None, *unpack_el(104, 118) ] for _ in range(size)],
    [None]*xlen,
    *[[*[None for _ in range(size*3)], None, *unpack_el(58, 71), *[None for _ in range(size)]] for _ in range(size)],
    *[[*[None for _ in range(size*3)], None, *unpack_el(90,103), *[None for _ in range(size)]] for _ in range(size)],
    ]

# Each Element gets a 2x2 square of cells. This allows for offsetting the Lanthanides/Actinides nicely
PERIODIC_TABLE_Z_2X2 = [
    [1,1, *[None for _ in range(33)], 2,2 ], 
    [1,1, *[None for _ in range(33)], 2,2 ], 
    [*unpack_el_range(3, 4),*[None for _ in range(21)], *unpack_el_range(5, 10)], 
    [*unpack_el_range(3, 4),*[None for _ in range(21)], *unpack_el_range(5, 10)], 
    [*unpack_el_range(11, 12),*[None for _ in range(21)], *unpack_el_range(13, 18)],  [*unpack_el_range(11, 12),*[None for _ in range(21)], *unpack_el_range(13, 18)],  [*unpack_el_range(19, 21), None, *unpack_el_range(22, 36)],  [*unpack_el_range(19, 21), None, *unpack_el_range(22, 36)],  
    [*unpack_el_range(37, 39), None, *unpack_el_range(40, 54)],  [*unpack_el_range(37, 39), None, *unpack_el_range(40, 54)],    
    [*unpack_el_range(55, 57), None, *unpack_el_range(72, 86)],  [*unpack_el_range(55, 57), None, *unpack_el_range(72, 86)],    
    [*unpack_el_range(87, 89), None, *unpack_el_range(104, 118)],    
    [*unpack_el_range(87, 89), None, *unpack_el_range(104, 118)],    
    [*[None for _ in range(7)], *unpack_el_range(58,71), None, None],  [*[None for _ in range(7)], *unpack_el_range(58,71), None, None],  [*[None for _ in range(7)], *unpack_el_range(90,103), None, None],  [*[None for _ in range(7)], *unpack_el_range(90,103), None, None],
]

# Output of annotate_periodic table:
PERIODIC_TABLE_ANNO = [
 ['H',1,"","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",'He',2],
 ['Hydrogen',"","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",'Helium',""],
 ['Li',3,'Be',4,"","","","","","","","","","","","","","","","","","","","","",'B',5,'C',6,'N',7,'O',8,'F',9,'Ne',10],
 ['Lithium',"",'Beryllium',"","","","","","","","","","","","","","","","","","","","","","",'Boron',"",'Carbon',"",'Nitrogen',"",'Oxygen',"",'Fluorine',"",'Neon',""],
 ['Na',11,'Mg',12,"","","","","","","","","","","","","","","","","","","","","",'Al',13,'Si',14,'P',15,'S',16,'Cl',17,'Ar',18],
 ['Sodium',"",'Magnesium',"","","","","","","","","","","","","","","","","","","","","","",'Aluminium',"",'Silicon',"",'Phosphorus',"",'Sulfur',"",'Chlorine',"",'Argon',""],
 ['K',19,'Ca',20,'Sc',21,"",'Ti',22,'V',23,'Cr',24,'Mn',25,'Fe',26,'Co',27,'Ni',28,'Cu',29,'Zn',30,'Ga',31,'Ge',32,'As',33,'Se',34,'Br',35,'Kr',36],
 ['Potassium',"",'Calcium',"",'Scandium',"","",'Titanium',"",'Vanadium',"",'Chromium',"",'Manganese',"",'Iron',"",'Cobalt',"",'Nickel',"",'Copper',"",'Zinc',"",'Gallium',"",'Germanium',"",'Arsenic',"",'Selenium',"",'Bromine',"",'Krypton',""],
 ['Rb',37,'Sr',38,'Y',39,"",'Zr',40,'Nb',41,'Mo',42,'Tc',43,'Ru',44,'Rh',45,'Pd',46,'Ag',47,'Cd',48,'In',49,'Sn',50,'Sb',51,'Te',52,'I',53,'Xe',54],
 ['Rubidium',"",'Strontium',"",'Yttrium',"","",'Zirconium',"",'Niobium',"",'Molybdenum',"",'Technetium',"",'Ruthenium',"",'Rhodium',"",'Palladium',"",'Silver',"",'Cadmium',"",'Indium',"",'Tin',"",'Antimony',"",'Tellurium',"",'Iodine',"",'Xenon',""],
 ['Cs',55,'Ba',56,'La',57,"",'Hf',72,'Ta',73,'W',74,'Re',75,'Os',76,'Ir',77,'Pt',78,'Au',79,'Hg',80,'Tl',81,'Pb',82,'Bi',83,'Po',84,'At',85,'Rn',86],
 ['Cesium',"",'Barium',"",'Lanthanum',"","",'Hafnium',"",'Tantalum',"",'Tungsten',"",'Rhenium',"",'Osmium',"",'Iridium',"",'Platinum',"",'Gold',"",'Mercury',"",'Thallium',"",'Lead',"",'Bismuth',"",'Polonium',"",'Astatine',"",'Radon',""],
 ['Fr',87,'Ra',88,'Ac',89,"",'Rf',104,'Db',105,'Sg',106,'Bh',107,'Hs',108,'Mt',109,'Ds',110,'Rg',111,'Cn',112,'Nh',113,'Fl',114,'Mc',115,'Lv',116,'Ts',117,'Og',118],
 ['Francium',"",'Radium',"",'Actinium',"","",'Rutherfordium',"",'Dubnium',"",'Seaborgium',"",'Bohrium',"",'Hassium',"",'Meitnerium',"",'Darmstadtium',"",'Roentgenium',"",'Copernicium',"",'Nihonium',"",'Flerovium',"",'Moscovium',"",'Livermorium',"",'Tennessine',"",'Oganesson',""],
 ["","","","","","","",'Ce',58,'Pr',59,'Nd',60,'Pm',61,'Sm',62,'Eu',63,'Gd',64,'Tb',65,'Dy',66,'Ho',67,'Er',68,'Tm',69,'Yb',70,'Lu',71,"",""],
 ["","","","","","","",'Cerium',"",'Praseodymium',"",'Neodymium',"",'Promethium',"",'Samarium',"",'Europium',"",'Gadolinium',"",'Terbium',"",'Dysprosium',"",'Holmium',"",'Erbium',"",'Thulium',"",'Ytterbium',"",'Lutetium',"","",""],
 ["","","","","","","",'Th',90,'Pa',91,'U',92,'Np',93,'Pu',94,'Am',95,'Cm',96,'Bk',97,'Cf',98,'Es',99,'Fm',100,'Md',101,'No',102,'Lr',103,"",""],
 ["","","","","","","",'Thorium',"",'Protactinium',"",'Uranium',"",'Neptunium',"",'Plutonium',"",'Americium',"",'Curium',"",'Berkelium',"",'Californium',"",'Einsteinium',"",'Fermium',"",'Mendelevium',"",'Nobelium',"",'Lawrencium',"","",""]
]

def deltafunc(size:int) -> list[tuple[int, int]]:
    """ return a list of (dx, dy) values for positioning annotations """
    assert size >= 1
    dxdy = []
    dxdy.append((0,0)) # Symbol: top left
    dxdy.append((size-1,0)) # Number: top right
    dxdy.append((size//2, size-1)) # bottom middle
    return dxdy

def annotate_periodic_table(tab=None, dfunc:Optional[Callable]=None):
    if tab is None:
        tab = PERIODIC_TABLE_Z_2X2
    
    ptdf = get_periodic_table_dataframe()
    pt_long = list(chain.from_iterable(tab))
    xlen, ylen = len(tab[0]), len(tab)
    # Get kernel size from ylen- table always has 9 full rows
    size = ylen // 9
    
    if dfunc is None:
        dfunc = partial(deltafunc, size)
    dxdy:list[tuple[int,int]] = dfunc()

    anno = [[""]*xlen for _ in range(ylen)]

    for sym, name, num in zip(ptdf['symbol'], ptdf['name'], ptdf['number']):        
        if num <= 118:
            loc = pt_long.index(num)

            x = loc % xlen
            y = loc // xlen
            
            for (dx,dy), val in zip(dxdy, (sym, num, name)):
                anno[y+dy][x+dx] = val
            
    return anno



def get_periodic_table_json(path:Optional[str]=None) -> dict:
    if path is None:
        path = PERIODIC_JSON_PATH
    with open(path, 'r', encoding="utf8") as f:
        periodic_table_json = json.load(f)
    return periodic_table_json


def get_periodic_table_dataframe(path:Optional[str]=None) -> dict:
    return pd.DataFrame.from_records(get_periodic_table_json(path)['elements'])


def periodic_table(size:int=3, layout:Optional[dict]=None) -> go.Figure:
    if layout is None:
        layout = PERIODIC_TABLE_LAYOUT

    tab = make_periodic_table_Z(size)
    anno = annotate_periodic_table(tab)

    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(
        z=tab[::-1], # Invert for plotting
        text=anno[::-1],
        texttemplate="%{text}",textfont={"size":8},
        hoverongaps = False, showscale=False,        
    ))

    fig.update_layout(**layout)

    return fig