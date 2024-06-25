# Copyright (c) 2010-2024, Lawrence Livermore National Security, LLC. Produced
# at the Lawrence Livermore National Laboratory. All Rights reserved. See files
# LICENSE and NOTICE for details. LLNL-CODE-443271.
#
# This file is part of the GLVis visualization tool and library. For more
# information and source code availability see https://glvis.org.
#
# GLVis is free software; you can redistribute it and/or modify it under the
# terms of the BSD-3 license. We welcome feedback and contributions, see file
# CONTRIBUTING.md for details.

import anywidget
import io
from IPython.display import display as ipydisplay
from traitlets import Unicode, Int, Bool
from typing import Union, Tuple
from pathlib import Path
import base64

try:
    from mfem._ser.mesh import Mesh
    from mfem._ser.gridfunc import GridFunction
except:
    Mesh = object
    GridFunction = object

Data = Union[Tuple[Mesh, GridFunction], Mesh, str]

def data_to_str(data: Data) -> str:
    if isinstance(data, str):
        return data

    sio = io.StringIO()
    if isinstance(data, tuple):
        sio.write("solution\n")
        data[0].WriteToStream(sio)
        data[1].WriteToStream(sio)
    elif isinstance(data, Mesh):
        sio.write("mesh\n")
        data.WriteToStream(sio)
    else:
        raise TypeError("Unknown data type")
    return sio.getvalue()

class _GlvisWidgetCore(anywidget.AnyWidget):
    """
    This is the backend that inherits from AnyWidget. Because we don't want all of the AnyWidget
    properties/methods exposed to the user, the front-end class GlvisWidget is a composition
    of this object, rather than directly inheriting from AnyWidget.

    _esm must be specified, and is basically a giant string with all of the javascript code required
    It could be defined as a docstring here, but for organization and syntax highlighting, it is
    defined in `widget.js`, similar to the organization used by pyobsplot:
    https://github.com/juba/pyobsplot/blob/main/src/pyobsplot/widget.py
    """
    _esm = anywidget._file_contents.FileContents(
        Path(__file__).parent / "widget.js", start_thread=False
    )

    data_str = Unicode('').tag(sync=True)
    width = Int(640).tag(sync=True)
    height = Int(480).tag(sync=True)
    is_new_stream = Bool().tag(sync=True)


class GlvisWidget:
    """
    Front-end class used to interactively visualize data.
    """
    def __init__(self, data: Data, width: int=640, height: int=480, keys=None):
        """
        Parameters
        ----------
        data : Union[Tuple[Mesh, GridFunction], Mesh, str]
            Data to be visualized. Can consist of the PyMFEM objects: (Mesh, GridFunction) or Mesh,
            or it can be read directly from a stream/string (see `examples/basic.ipynb`).
        width : int, optional
            Width of visualization
        height : int, optional
            Height of visualization
        keys : str, optional
            Keyboard commands to customize the visualization. Can also be typed into the widget
            after it is instantiated. For a full list of options, see the GLVis README:
            https://github.com/GLVis/glvis?tab=readme-ov-file#key-commands
        """

        self._widget = _GlvisWidgetCore()
        self.set_size(width, height)
        self._sync(data, is_new=True, keys=keys)

    # Automatically renders the widget - necessary because this is a wrapper class
    def _repr_mimebundle_(self, *args, **kwargs):
        return self._widget._repr_mimebundle_(*args, **kwargs)

    def set_size(self, width: int, height: int):
        self._widget.width = width
        self._widget.height = height

    def plot(self, data: Data, keys=None):
        self._sync(data, is_new=True, keys=keys)

    def update(self, data: Data, keys=None):
        self._sync(data, is_new=False, keys=keys)

    def _on_msg(self, _, content, buffers):
        if content.get("type", "") == "screenshot":
            data = content.get("b64", "")
            name = content.get("name", "glvis.png")
            if not data:
                print(f"unable to save {name}, bad data")
                return
            with open(name, "wb") as f:
                f.write(base64.decodebytes(data.encode('ascii')))

    def _sync(self, data: Data, is_new: bool=True, keys=None):
        self._widget.is_new_stream = is_new
        data_string = data_to_str(data)
        if keys is not None:
            key_string = keys if isinstance(data, str) else f"keys {keys}"
            data_string += key_string
        self._widget.data_str = data_string

    def render(self):
        ipydisplay(self)

# Constructor alias
def glvis(data: Data, width: int=640, height: int=480, keys=None):
    return GlvisWidget(data, width, height, keys)
glvis.__doc__ = GlvisWidget.__init__.__doc__