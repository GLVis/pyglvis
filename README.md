# Interactive GLVis Jupyter Widget

<!-- Badges generated at https://mybinder.readthedocs.io/en/latest/howto/badges.html -->
[![badge](examples/basic.svg "Basic GLVis + Jupyter Example")](https://mybinder.org/v2/gh/GLVis/pyglvis/anywidget?filepath=examples%2Fbasic.ipynb)
[![badge](examples/plot.svg "Plot grid functions")](https://mybinder.org/v2/gh/GLVis/pyglvis/anywidget?filepath=examples%2Fplot.ipynb)
[![badge](examples/ex1.svg "MFEM's Example 1")](https://mybinder.org/v2/gh/GLVis/pyglvis/anywidget?filepath=examples%2Fex1.ipynb)
[![badge](examples/ex9.svg "MFEM's Example 9")](https://mybinder.org/v2/gh/GLVis/pyglvis/anywidget?filepath=examples%2Fex9.ipynb)

This repository contains a [Jupyter](https://jupyter.org/) widget for the [GLVis](https://glvis.org/) finite element
visualization tool based on the [glvis-js](https://github.com/GLVis/glvis-js) JavaScript/WebAssembly library.

## Usage

```python
from glvis import glvis

glvis(data, [width=640, height=480, keys=None])

# or assign if you want to update later
g = glvis(data)
# run a cell with `g` to show it
g
```

The `data` object can be one of:

- a `str`, in the format of `*.saved` files
- a `Mesh`, defined in [PyMFEM](https://github.com/mfem/pymfem)
- a `(Mesh, GridFunction)` tuple, defined in [PyMFEM](https://github.com/mfem/pymfem)

[PyMFEM](https://github.com/mfem/pymfem) can be installed with `pip install mfem`.


Once you have a `glvis` object there are a few methods that can used to update the
visualization:
```python
# show a new Mesh/GridFunction, resets keys
g.plot(data)
# show an updated visualization with the same `Mesh` and `GridFunction`
# dimensions, preserves keys
g.update(data)
# change the image size
g.set_size(width, height)
# force the widget to render. if the widget isn't the last statement in a cell it
# will not be shown without this. see ex9.ipynb
g.render()
```

See the [examples](examples/) directory for additional examples. To test those locally, start a Jupyter notebook server with

```
jupyter notebook
```

## Installation

The GLVis Jupyter widget can be simply installed with `pip`:

```
pip install pyglvis
```


## Development

`pyglvis` pulls the latest version of `glvis-js` from `npm` in the first line of `/glvis/widget.js`: 
`import glvis from "https://esm.sh/glvis";`

If you want to use a specific version, simply add `@x.y.z` to the end of the import statement, where `x.y.z` matches a version number available on `npm`, e.g.
`import glvis from "https://esm.sh/glvis@0.6.3";`



## Releasing

### Releasing a new version of glvis on NPM:

To publish a new version of `glvis-js`, follow the instructions on the `glvis-js`.


### Releasing a new version of glvis on PyPI:

- Update `__version__` in `glvis/__about__.py` 

- `git add` and `git commit` changes


You will need [twine](https://pypi.org/project/twine/) to publish to PyPI, install with `pip`.

```
python setup.py sdist bdist_wheel
twine upload dist/*
git tag -a X.X.X -m 'comment'
git push --tags
```
