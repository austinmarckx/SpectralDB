
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
from typing import Optional, Union, Callable
from functools import partial
from spectraldb.utils.types import Element
from spectraldb.utils.preprocess import preprocess, filter_visible
from spectraldb.utils.misc import uno_reverse

DEFAULT_LAYOUT = {
    "template":"simple_white",
    "font":{'family': "Times New Roman", "size": 24},
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


