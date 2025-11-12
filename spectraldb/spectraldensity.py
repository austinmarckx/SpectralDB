
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from functools import lru_cache
from typing import Optional, Union, Callable, Literal
from spectraldb.utils.io import load_cie_reference, get_element_name
from spectraldb.utils.types import Element, CIEReference, Colorscale 
from spectraldb.utils.preprocess import preprocess, filter_visible
from spectraldb.utils.misc import uno_reverse
from spectraldb.colorspaces import make_colorscale, normalize_wavelength, XYZ_to_color

DEFAULT_LAYOUT = {
    "template":"simple_white",
    "font":{'family': "Times New Roman", "size": 24},
}

DEFAULT_LAYOUT_SPECTRAL_BANDS = {
    **DEFAULT_LAYOUT,
    "title":{"text":"Element Spectral Bands: 0.1 nm stepsize" },
    "xaxis":{"title": "Wavelength (nm)", "automargin":True },
}

DEFAULT_LAYOUT_SPECTRAL_DENSITY = {
    **DEFAULT_LAYOUT,
    "title":{"text":"Element Spectral Density" },
    "yaxis":{"title": "density", "automargin":True },
    "xaxis":{"title": "Wavelength (nm)", "automargin":True },
}

def _process_input_for_spectral_density(el:Optional[Union[Element, list[Element]]]=None, data:Optional[pd.DataFrame]=None, func:Optional[Callable]=None) -> tuple[list, list]:
    if func is None:
        func = uno_reverse
    labs = None
    
    if el is not None:    
        if not isinstance(el, list):
            data = [func(el)]
            labs = [el]
        else:
            data = list(map(func, el))
            labs = el
    elif data is not None:
        if not isinstance(data, list):
            data = [data]
            labs = ["Element"]
    else:
        raise ValueError

    return data, labs

def visible_spectral_density(*args, **kwargs):
    return spectral_density(visible=True, *args, **kwargs)

def spectral_density(el:Optional[Union[Element, list[Element]]]=None, data:Optional[pd.DataFrame]=None, visible:bool=False, *args, **kwargs) -> go.Figure: 
    func = kwargs.get("func", None)
    if visible:
        func = lambda curr: filter_visible(preprocess(curr, trimmed=True))['wavelength_nm'].tolist()
    else:
        func = lambda curr: preprocess(curr, trimmed=True)['wavelength_nm'].tolist()
    data, labs = _process_input_for_spectral_density(el, data, func)
    
    fig = ff.create_distplot(data, labs, **kwargs)
    
    fig.update_layout(
        **DEFAULT_LAYOUT_SPECTRAL_DENSITY
    )

    return fig


def spectrum_walk(stepsize:float=0.1, minval:float=390, maxval:float=830):
    spect = np.linspace(minval, maxval, num=int((maxval-minval)/stepsize)).tolist()
    return spect

def reference_heatmap(el:Optional[Union[Element, list[Element]]]=None, minval=390, maxval=700, **kwargs):
    return heatmap(el, colorscale="reference", showscale=False, minval=minval, maxval=maxval, **kwargs)

def heatmap(
        el:Optional[Union[Element, list[Element]]]=None, minval:float=390, maxval:float=830,
        colorscale:Colorscale="viridis", showscale:bool=True, reference:Optional[CIEReference]=None, 
    **kwargs) -> go.Figure: 
    layout = kwargs.get("layout", DEFAULT_LAYOUT_SPECTRAL_BANDS)
    data, labs = [], []

    ref = load_cie_reference(refdeg=reference)
    ref = ref[(ref["wavelength_nm"] >= minval) & (ref["wavelength_nm"] <= maxval)]
    wl = ref['wavelength_nm'].tolist()
    
    cs = colorscale
    if colorscale == "reference":
        cs = make_colorscale(ref)
        labs.append(reference if reference is not None else "CIE 2006 Deg 2")
        data.append(wl)
        showscale = False      
        

    def func(el) -> tuple[list[float], Colorscale]:
        df = filter_visible(preprocess(el, trimmed=True))
        f = lambda v1: df[(df["wavelength_nm"] >= v1-0.05) & (df["wavelength_nm"] <= v1+0.05)]
        g = lambda v2: f(v2).shape[0]
        h = lambda v3: np.log10(f(v3)['intensity'].sum()+1)
        if colorscale == "reference":
            return [wave_bin if g(wave_bin) else minval for wave_bin in spectrum_walk(0.1, minval=minval, maxval=maxval)]        
        return [h(wave_bin) if g(wave_bin) else 0 for wave_bin in spectrum_walk(0.1, minval=minval, maxval=maxval)]

    if el is not None:    
        if isinstance(el, str):
            data += [func(el)]
            labs += [get_element_name(el)]
        else:
            data += list(map(func, el))
            labs += list(map(get_element_name, el))
       
    
    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(
        y=labs, x=wl, z=data, colorscale=cs, showscale=showscale,
        colorbar={"title":{"text":"log10(intensity)", "side":"top", "font":{"size": 18},}}, **kwargs
    ))

    fig.update_layout(**layout)

    return fig
