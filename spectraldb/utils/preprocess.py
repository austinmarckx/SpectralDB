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

Relative intensity tags:

Descriptors to the relative intensities have the following meaning:

     *    Intensity is shared by several lines (typically, for multiply classified lines).
     :    Observed value given is actually the rounded Ritz value, e.g., Ar IV, λ = 443.40 Å.
     -    Somewhat lower intensity than the value given.
     a    Observed in absorption.
     b    Band head.
     bl   Blended with another line that may affect the wavelength and intensity.
     B    Line or feature having large width due to autoionization broadening.
     c    Complex line.
     d    Diffuse line.
     D    Double line.
     E    Broad due to overexposure in the quoted reference
     f    Forbidden line.
     g    Transition involving a level of the ground term.
     G    Line position roughly estimated.
     H    Very hazy line.
     h    Hazy line (same as "diffuse").
     hfs  Line has hyperfine structure.
     i    Identification uncertain.
     j    Wavelength smoothed along isoelectronic sequence.
     l    Shaded to longer wavelengths; NB: This may look like a "one" at the end
          of the number!
     m    Masked by another line (no wavelength measurement).
     p    Perturbed by a close line. Both wavelength and intensity may be affected.
     q    Asymmetric line.
     r    Easily reversed line.
     s    Shaded to shorter wavelengths.
     t    Tentatively classified line.
     u    Unresolved from a close line.
     w    Wide line.
     x    Extrapolated wavelength

"""
import numpy as np
import pandas as pd
from typing import Optional

from spectraldb.utils.types import Element
from spectraldb.utils.io import load_element

COLUMN_MAP = {
    "element":"element",
    "sp_num":"spectrum_number",
    "obs_wl_vac(nm)":"wavelength_nm",
    "intens_value":"intensity",
    "log_intens":"log10_intensity",
    "intens_tags":"tags"
}

COLUMN_TYPES = {
    "element":str,
    "spectrum_number":int,
    "wavelength_nm":float,
    "intensity":float,
    "log10_intensity":float,
    "tags":str
}

def preprocess(el:Element, trimmed:bool=False) -> pd.DataFrame:
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
    ## Most Elements will have 3 columns, however, some of the larger elements don't have data there.
    ## Use shape of df as check. o/w just leave the None place holders.
    df["intens_value"] = None
    df["log_intens"] = None
    df["intens_tags"] = None

    if tmp.shape[1] > 1:
        df['intens_value'] = tmp[1]
        df['log_intens'] = df['intens_value'].astype(float).apply(np.log10)
    if tmp.shape[1] > 2:
        df['intens_tags'] = tmp[0] + tmp[2]

    if trimmed:
        return trim(df)
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

def trim(df:pd.DataFrame) -> pd.DataFrame:
    """ Subset and """
    df = _subset_rename(df)
    df = df.dropna(subset=["wavelength_nm","intensity","log10_intensity"])
    df = _type_conversion(df)
    df["visible"] = (df['wavelength_nm'] >= 300) & (df['wavelength_nm'] <= 800)
    return df


def _type_conversion(df:pd.DataFrame, mapping:Optional[dict[str,str]]=None) -> pd.DataFrame:
    if mapping is None:
        mapping = COLUMN_TYPES
    
    for col, ty in mapping.items():
        try:
            df[col] = [val if val != '' else None for val in df[col]]
            df[col] = df[col].astype(ty)
        except Exception as e:
            print(f"Unable to convert `{col}` with exception: `{e}`")

    return df

def _subset_rename(df:pd.DataFrame, mapping:Optional[dict[str,str]]=None) -> pd.DataFrame:
    if mapping is None:
        mapping = COLUMN_MAP
    return df[list(mapping.keys())].rename(columns=mapping)
    
