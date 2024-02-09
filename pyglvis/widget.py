import anywidget
import io
from traitlets import Unicode, Int, Bool
from pathlib import Path

# Import file contents example: https://github.com/juba/pyobsplot/blob/main/src/pyobsplot/widget.py
class Glvis(anywidget.AnyWidget):
    _esm = anywidget._file_contents.FileContents(
        Path(__file__).parent / "widget.js", start_thread=False
    )

    data_str = Unicode('').tag(sync=True)
    data_type = Unicode('').tag(sync=True)
    width = Int(640).tag(sync=True)
    height = Int(480).tag(sync=True)
    is_new_stream = Bool().tag(sync=True)

