""" 
For detailed information about the original data see:
https://physics.nist.gov/PhysRefData/ASD/Html/lineshelp.html

Disclaimer: 
This repo is not intended to be a highly faithful replacement for the Atomic
Spectra Database (ASD).
The primary down stream applications are intended to be qualitative. As such,
much of the detail (while interesting) is not relevant and there may be errors 
introduced during preprocessing. Use at your own risk.

Notes:
1) I will not making the distinction between vaccuum and air.
- This level of detail is simply not required
2) I will introduce `element` and `ion` columns for elements if they do not exist.
- These values may or may not reflect real states of matter
3) Accuracy encoding map:
    AAA	≤	0.3%
    AA	≤	1%
    A+	≤	2%
    A	≤	3%
    B+	≤	7%
    B	≤	10%
    C+	≤	18%
    C	≤	25%
    D+	≤	40%
    D	≤	50%
    E	>	50%.
"""
import numpy as np
import pandas as pd
from utils.types import Element
from utils.io import load_element

def preprocess(el:Element) -> pd.DataFrame:
    df = None
    try:
        # 1) Load data
        df = load_element(el)
    except Exception as e:
        raise e("Error loading element from disk")
    
    # 2) Drop table differentiation between vaccuum and air
    df = drop_intermediate_tables(df)

    # 3) Element/Ion columns
    if "element" not in df.columns:
        df['element'] = el
    if "sp_num" not in df.columns:
        df['sp_num'] = 0

    # 4) `None` & float parsing
    df = df.map(cell_parser)

    # 5) Relative intensity flag parsing
    ## Relative intensity digit:
    tmp = df['intens'].str.split(r"^(\d+)", expand=True)
    df['intens_value'] = tmp[1]
    df['log_intens'] = df['intens_value'].astype(float).apply(np.log10)
    df['intens_tags'] = tmp[0] + tmp[2]
    return df
    
def cell_parser(value):
    if isinstance(value, str):
        return value.lstrip('="').rstrip('"')
    return value

def drop_intermediate_tables(df:pd.DataFrame) -> pd.DataFrame:
    """
    Best I can tell, all rows have an accuracy value.
    If the accuracy value == Acc, this represents the head of a new table.
    Drop these rows.
    """
    return df[df['line_ref'] != "line_ref"]