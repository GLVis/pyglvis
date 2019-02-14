pyglvis
=======

Interactive finite element visualization widget for the Jupyter Notebook,
built from [GLVis](https://glvis.org).

Usage
-----

```python
from pyglvis import GlvisWidget
GlvisWidget(stream[, width=640, height=480])
# or assign if you want to update later
g = GlvisWidget(stream)
# run a cell with `g` to show it
g
# updates will update the original widget
g.update(stream)
```

Installation
------------

To install with pip:

```bash
pip install pyglvis
jupyter nbextension enable --py pyglvis
# jupyter lab
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyter-glvis
```


For a development installation (requires npm):

```bash
git clone https://github.com/glvis/glvis-widget.git
cd pyglvis
pip install -e .
jupyter nbextension install --py --symlink --sys-prefix pyglvis
jupyter nbextension enable --py --sys-prefix pyglvis
# jupyter lab
jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build
jupyter labextension link ./js
```
