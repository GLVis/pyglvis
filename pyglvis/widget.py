import ipywidgets as widgets
import json
import os
from traitlets import Unicode, Int, Bool

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

    def _set_stream(self, stream, new=True):
        offset = stream.find("\n")
        self._data_type = stream[0:offset]
        self._data_str = stream[offset + 1:]
        self._new_stream = new

    def __init__(self, stream, width=640, height=480, *args, **kwargs):
        widgets.DOMWidget.__init__(self, *args, **kwargs)
        self._width = width
        self._height = height
        self._set_stream(stream)

    def new_vis(self, stream):
        self._set_stream(stream)

    def update(self, stream):
        self._set_stream(stream, False)
