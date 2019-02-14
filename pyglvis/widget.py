import ipywidgets as widgets
import json
import os
from traitlets import Unicode, Int

here = os.path.dirname(__file__)
with open(os.path.join(here, "static", "package.json")) as f:
    version = json.load(f)["version"]


@widgets.register
class GlvisWidget(widgets.DOMWidget):
    _model_name = Unicode('GlvisModel').tag(sync=True)
    _model_module = Unicode('jupyter-glvis').tag(sync=True)
    _model_module_version = Unicode('^' + version).tag(sync=True)

    _view_name = Unicode('GlvisView').tag(sync=True)
    _view_module = Unicode('jupyter-glvis').tag(sync=True)
    _view_module_version = Unicode('^' + version).tag(sync=True)

    _data_str = Unicode().tag(sync=True)
    _data_type = Unicode().tag(sync=True)
    _width = Int().tag(sync=True)
    _height = Int().tag(sync=True)

    def _set_state(self, stream):
        offset = stream.find('\n')
        self._data_type = stream[0:offset]
        self._data_str = stream[offset+1:]

    def __init__(self, stream, width=640, height=480, *args, **kwargs):
        widgets.DOMWidget.__init__(self, *args, **kwargs)
        self._width = width
        self._height = height
        self._set_state(stream)

    def update(self, stream):
        self._set_state(stream)
