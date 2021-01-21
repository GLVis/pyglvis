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

import ipywidgets as widgets
from IPython.display import display as ipydisplay
from traitlets import Unicode, Int, Bool
from ._version import extension_version

try:
    from mfem._ser.mesh import Mesh
    from mfem._ser.gridfunc import GridFunction
except ImportError:
    Mesh = object
    GridFunction = object


def to_stream(mesh: Mesh, gf: GridFunction = None) -> str:
    stream = "solution\n" if gf is not None else "mesh\n"
    temp_file = "temp.saved"
    mesh.Print(temp_file)
    with open(temp_file, "r") as f:
        stream += f.read()
    if gf is not None:
        stream += "\n"
        gf.Save(temp_file)
        with open(temp_file, "r") as f:
            stream += f.read()
    return stream


@widgets.register
class glvis(widgets.DOMWidget):
    _model_name = Unicode("GLVisModel").tag(sync=True)
    _model_module = Unicode("glvis-jupyter").tag(sync=True)
    _model_module_version = Unicode("^" + extension_version).tag(sync=True)

    _view_name = Unicode("GLVisView").tag(sync=True)
    _view_module = Unicode("glvis-jupyter").tag(sync=True)
    _view_module_version = Unicode("^" + extension_version).tag(sync=True)

    _data_str = Unicode().tag(sync=True)
    _data_type = Unicode().tag(sync=True)
    _width = Int().tag(sync=True)
    _height = Int().tag(sync=True)
    _is_new_stream = Bool().tag(sync=True)

    def _sync(self, data, is_new=True):
        self._is_new_stream = is_new
        if isinstance(data, str):
            stream = data
        elif isinstance(data, tuple):
            stream = to_stream(*data)
        elif isinstance(data, Mesh):
            stream = to_stream(data)
        else:
            raise TypeError
        offset = stream.find("\n")
        self._data_type = stream[0:offset]
        self._data_str = stream[offset + 1:]

    def __init__(self, data, width=640, height=480, *args, **kwargs):
        widgets.DOMWidget.__init__(self, *args, **kwargs)
        self.set_size(width, height)
        self._sync(data, is_new=True)

    def display(self, data):
        self._sync(data, is_new=True)

    def update(self, data):
        self._sync(data, is_new=False)

    def set_size(self, width, height):
        self._width = width
        self._height = height

    def show(self):
        ipydisplay(self)

    def serialize(self):
        """Return dict that can be used to construct a copy of this instance

        glvis(**other.serialize())
        """
        return {"data": self._data_type + "\n" + self._data_str,
                "width": self._width, "height": self._height}
