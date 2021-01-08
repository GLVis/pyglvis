# Interactive Visualization Widget build on glvis-js

## Usage

```python
from glvis import GLVisWidget
GLVisWidget(stream[, width=640, height=480])
# or assign if you want to update later
g = GLVisWidget(stream)
# run a cell with `g` to show it
g

# other methods
g.new_vis(stream)
g.update(stream)
g.set_size(width, height)
```

## Installation

```bash
pip install glvis
```

After installing it's good to verify that the notebook extensions are actually working:

```
jupyter nbextension list
```

Which should look something like:

```
Known nbextensions:
  config dir: .../nbconfig
    notebook section
      glvis-jupyter/extension  enabled
      - Validating: OK
      jupyter-js-widgets/extension  enabled
      - Validating: OK
```

If you do not see both `glvis-jupyter` and `jupyter-js-widgets` then try the following:

```
jupyter nbextension install --user --py glvis
jupyter nbextension enable --user --py glvis
jupyter nbextension install --user --py widgetsnbextension
jupyter nbextension enable --user --py widgetsnbextension
```

Jupyter Lab requires another set of install commands:
TODO test, only for Lab 2.

```
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install glvis-jupyter
```

### Development

Development installation requires npm, webpack, and webpack-cli and hasn't been tested much.
After you have npm installed, install webpack and webpack-cli (globally) with (TODO is this actually
needed?):

```shell
npm install -g webpack webpack-cli
```

Then you should be able to install glvis:

```bash
git clone https://github.com/glvis/pyglvis.git
cd pyglvis
pip install -e .

# notebook
jupyter nbextension install --py --symlink --sys-prefix glvis
jupyter nbextension enable --py --sys-prefix glvis

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
