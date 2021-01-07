# pyglvis

Interactive finite element visualization widget for the Jupyter Notebook,
built from [GLVis](https://glvis.org).

## Usage

```python
from pyglvis import GLVisWidget
GlvisWidget(stream[, width=640, height=480])
# or assign if you want to update later
g = GLVisWidget(stream)
# run a cell with `g` to show it
g
# updates will update the original widget
g.update(stream)
```

## Installation

To install with pip:

```bash
pip install pyglvis

# notebook
jupyter nbextension enable --py pyglvis

# jupyter lab
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install glvis-jupyter
```

### Development

Development installation requires npm, webpack, and webpack-cli and hasn't been tested much.
After you have npm installed, install webpack and webpack-cli (globally) with:

```shell
npm install -g webpack webpack-cli
```

Then you should be able to install pyglvis:

```bash
git clone https://github.com/glvis/pyglvis.git
cd pyglvis
pip install -e .

# notebook
jupyter nbextension install --py --symlink --sys-prefix pyglvis
jupyter nbextension enable --py --sys-prefix pyglvis

# jupyter lab
jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build
jupyter labextension link ./js
```

If you run into errors related to npm that aren't helpful my suggestion would be to:

```shell
cd pyglvis
make clean
cd js
npm install
npx webpack
```

And handle errors/deal with command line questions from there.
