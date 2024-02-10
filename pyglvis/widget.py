import anywidget
import io
from traitlets import Unicode, Int, Bool
from typing import Union, Tuple
from pathlib import Path

from mfem._ser.mesh import Mesh
from mfem._ser.gridfunc import GridFunction

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

# Import file contents example: https://github.com/juba/pyobsplot/blob/main/src/pyobsplot/widget.py
class GlvisWidget(anywidget.AnyWidget):
    _esm = anywidget._file_contents.FileContents(
        Path(__file__).parent / "widget.js", start_thread=False
    )

    data_str = Unicode('').tag(sync=True)
    width = Int(640).tag(sync=True)
    height = Int(480).tag(sync=True)
    is_new_stream = Bool().tag(sync=True)


# The purpose of this wrapper class is to keep the API of Glvis clean by excluding inherited properties/methods 
class Glvis:
    widget = GlvisWidget()

    # Automatically renders the widget - necessary because this is a wrapper class
    def _repr_mimebundle_(self, *args, **kwargs):
        return self.widget._repr_mimebundle_(*args, **kwargs)

    def __init__(self, data: Data, width: int = 640, height: int = 480):
        self.set_size(width, height)
        self._sync(data, is_new=True)

    def set_size(self, width: int, height: int):
        self.widget.width = width
        self.widget.height = height

    def _sync(self, data: Data, is_new: bool = True):
        self.widget.is_new_stream = is_new
        self.widget.data_str = data_to_str(data)