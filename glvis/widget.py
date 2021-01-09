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
import json
import os
from traitlets import Unicode, Int, Bool

try:
    import mfem
    from mfem._ser.mesh import Mesh
    from mfem._ser.gridfunc import GridFunction
except ImportError:
    mfem = None
    pass


# TODO: TMS
"""
here = os.path.dirname(__file__)
with open(os.path.join(here, "nbextension", "package.json")) as f:
    version = json.load(f)["version"]
    """
version = "0.1.0"


@widgets.register
class GLVisWidget(widgets.DOMWidget):
    _model_name = Unicode("GLVisModel").tag(sync=True)
    _model_module = Unicode("glvis-jupyter").tag(sync=True)
    _model_module_version = Unicode("^" + version).tag(sync=True)

    _view_name = Unicode("GLVisView").tag(sync=True)
    _view_module = Unicode("glvis-jupyter").tag(sync=True)
    _view_module_version = Unicode("^" + version).tag(sync=True)

    _data_str = Unicode().tag(sync=True)
    _data_type = Unicode().tag(sync=True)
    _width = Int().tag(sync=True)
    _height = Int().tag(sync=True)
    _new_stream = Bool().tag(sync=True)

    def _display_stream(self, stream, new=True):
        offset = stream.find("\n")
        self._data_type = stream[0:offset]
        self._data_str = stream[offset + 1 :]
        self._new_stream = new

    def __init__(self, stream, width=640, height=480, *args, **kwargs):
        widgets.DOMWidget.__init__(self, *args, **kwargs)
        set_size(width, height)
        self._set_stream(stream)

    def display(self, stream):
        self._display_stream(stream)

    def update(self, stream):
        self._display_stream(stream, False)

    def set_size(self, width, height):
        self._width = width
        self._height = height

    if mfem:
        # TODO: validate args, updates to MFEM so we don't need a temp file
        def _to_stream(self, mesh, gf=None):
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

        def __init__(self, mesh, gf=None, width=640, height=480, *args, **kwargs):
            widgets.DOMWidget.__init__(self, *args, **kwargs)
            self.set_size(width, height)
            self.display2(mesh, gf)

        # TODO: one display and update that checks arg types
        def display2(self, mesh, gf):
            self.display(self._to_stream(mesh, gf))

        def update2(self, mesh, gf):
            self.update(self._to_stream(mesh, gf))
