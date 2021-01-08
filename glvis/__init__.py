from ._version import version_info, __version__
from .widget import GLVisWidget


def _jupyter_nbextension_paths():
    return [
        {
            "section": "notebook",
            "src": "nbextension",
            "dest": "glvis-jupyter",
            "require": "glvis-jupyter/extension",
        }
    ]
