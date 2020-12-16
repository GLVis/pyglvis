from ._version import version_info, __version__
from .widget import GlvisWidget


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'glvis-jupyter',
        'require': 'glvis-jupyter/extension'
    }]
