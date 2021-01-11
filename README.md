# Interactive GLVis Jupyter Widget

This repository contains a [Jupyter](https://jupyter.org/) widget for the [GLVis](https://glvis.org/) finite element visualization tool based on the [glvis-js](https://github.com/GLVis/glvis-js) JavaScript/WebAsembly library.

## Usage

```python
from glvis import GLVisWidget

GLVisWidget(stream[, width=640, height=480])

# or assign if you want to update later
g = GLVisWidget(stream)
# run a cell with `g` to show it
g

# other methods
g.display(stream)
g.update(stream)
g.set_size(width, height)
```

If [PyMFEM](https://github.com/mfem/pymfem) is installed  (`pip install mfem --no-binary mfem`) you can also use the `Mesh` and `GridFunction` arguments.

```python
GLVisWidget(Mesh[, GridFunction])
```

## Installation

The GLVis Jupyter widget can be simply installed with `pip` and enabled with `jupyter nbextension enable`.


```bash
pip install glvis
jupyter nbextension enable --py glvis
```

After installing you can verify that the notebook extensions are working with

```
jupyter nbextension list
```

The output should be something like

```
Known nbextensions:
  config dir: path/to/nbconfig
    notebook section
      glvis-jupyter/extension  enabled
      - Validating: OK
  <possibly a different config dir>
      jupyter-js-widgets/extension  enabled
      - Validating: OK
```

If `glvis-jupyter` and `jupyter-js-widgets` are not both listed, try the following:

```
jupyter nbextension install --user --py glvis
jupyter nbextension enable --user --py glvis
jupyter nbextension install --user --py widgetsnbextension
jupyter nbextension enable --user --py widgetsnbextension
```

[JupyterLab](https://jupyterlab.readthedocs.io) requires another set of install commands:

```
jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build
jupyter labextension install glvis-jupyter
```

## Development

Development installation requires `npm`, `webpack`, and `webpack-cli` and has not been tested extensively. After `npm` is installed, install `webpack` and `webpack-cli` (globally) with **(TODO is this actually needed?)**:

```shell
npm install -g webpack webpack-cli
```

Then you should be able to install glvis as follows

```bash
git clone https://github.com/glvis/pyglvis.git
cd pyglvis
pip install -e .

# notebook
jupyter nbextension install --py --symlink --sys-prefix glvis
jupyter nbextension enable --py --sys-prefix glvis

# jupyter lab
jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build
# I believe you need node in the path Lab uses for this to work, I see an extension load error
# in a context where I don't have it:
# Failed to load resource: the server responded with a status of 500 (Internal Server Error)
#   lab/api/extensions?1610138347763
# Which is just a python stacktrace, ending with:
#   raise ValueError(msg)\nValueError: Please install Node.js and npm before continuing installation. 
jupyter labextension link ./js
```

If you run into errors related to node/npm that aren't helpful try:

```shell
cd pyglvis
make clean
cd js
npm install
npx webpack
```

## Releasing a new version of glvis on PyPI:

- Update `_version.py` (set release version, remove `dev`)
- Update `model/view` version in `widget.py`
- `git add` the `_version.py` file and `git commit`

```bash
python setup.py sdist upload
python setup.py bdist_wheel upload
git tag -a X.X.X -m 'comment'
```

- Update `_version.py` (add `dev` and increment minor):

```bash
git add and git commit
git push
git push --tags
```

## Releasing a new version of glvis-jupyter on NPM:

Update model/view version in `widget.js`

```console
# clean out the `dist` and `node_modules` directories
git clean -fdx
npm install
npm publish
```
