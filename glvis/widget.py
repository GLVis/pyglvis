# Copyright (c) 2010-2021, Lawrence Livermore National Security, LLC. Produced
# at the Lawrence Livermore National Laboratory. All Rights reserved. See files
# LICENSE and NOTICE for details. LLNL-CODE-443271.
#
# This file is part of the GLVis visualization tool and library. For more
# information and source code availability see https://glvis.org.
#
# GLVis is free software; you can redistribute it and/or modify it under the
# terms of the BSD-3 license. We welcome feedback and contributions, see file
# CONTRIBUTING.md for details.

import io
import ipywidgets as widgets
from IPython.display import display as ipydisplay
from traitlets import Unicode, Int, Bool
from typing import Union, Tuple
from ._version import extension_version
import base64

try:
    from mfem._ser.mesh import Mesh
    from mfem._ser.gridfunc import GridFunction
except ImportError:
    Mesh = object
    GridFunction = object

Stream = Union[Tuple[Mesh, GridFunction], Mesh, str]


def to_stream(mesh: Mesh, gf: GridFunction = None) -> str:
    sio = io.StringIO()
    sio.write("solution\n" if gf is not None else "mesh\n")
    mesh.WriteToStream(sio)
    if gf:
        gf.WriteToStream(sio)
    return sio.getvalue()


@widgets.register
class glvis(widgets.DOMWidget):
    _model_name = Unicode("GLVisModel").tag(sync=True)
    _model_module = Unicode("glvis-jupyter").tag(sync=True)
    _model_module_version = Unicode("^" + extension_version).tag(sync=True)

    _view_name = Unicode("GLVisView").tag(sync=True)
    _view_module = Unicode("glvis-jupyter").tag(sync=True)
    _view_module_version = Unicode("^" + extension_version).tag(sync=True)

    data_str = Unicode().tag(sync=True)
    data_type = Unicode().tag(sync=True)
    width = Int().tag(sync=True)
    height = Int().tag(sync=True)
    is_new_stream = Bool().tag(sync=True)

    def _sync(self, data: Stream, is_new: bool = True):
        self.is_new_stream = is_new
        if isinstance(data, str):
            stream = data
        elif isinstance(data, tuple):
            stream = to_stream(*data)
        elif isinstance(data, Mesh):
            stream = to_stream(data)
        else:
            raise TypeError
        offset = stream.find("\n")
        self.data_type = stream[0:offset]
        self.data_str = stream[offset + 1:]

    def _on_msg(self, _, content, buffers):
        if content.get("type", "") == "screenshot":
            data = content.get("b64", "")
            name = content.get("name", "glvis.png")
            if not data:
                print(f"unable to save {name}, bad data")
                return
            with open(name, "wb") as f:
                f.write(base64.decodebytes(data.encode('ascii')))

    def __init__(
        self, data: Stream, width: int = 640, height: int = 480, *args, **kwargs
    ):
        widgets.DOMWidget.__init__(self, *args, **kwargs)
        self.set_size(width, height)
        self._sync(data, is_new=True)
        self.on_msg(self._on_msg)

    def plot(self, data: Stream):
        self._sync(data, is_new=True)

    def update(self, data: Stream):
        self._sync(data, is_new=False)

    def set_size(self, width: int, height: int):
        self.width = width
        self.height = height

    def render(self):
        ipydisplay(self)

    def screenshot(self, name, use_web=False):
        self.send({"type": "screenshot", "name": name, "use_web": use_web})

    def serialize(self):
        """Return dict that can be used to construct a copy of this instance

        glvis(**other.serialize())
        """
        return {
            "data": self.data_type + "\n" + self.data_str,
            "width": self.width,
            "height": self.height,
        }
