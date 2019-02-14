## Releasing a new version of pyglvis on PyPI:

Update \_version.py (set release version, remove 'dev')
Update model/view version in widget.py 
git add the \_version.py file and git commit

```bash
python setup.py sdist upload
python setup.py bdist_wheel upload
git tag -a X.X.X -m 'comment'
```

Update \_version.py (add 'dev' and increment minor):

```bash
git add and git commit
git push
git push --tags
```

## Releasing a new version of jupyter-glvis on NPM:

Update model/view version in widget.js

```console
# clean out the `dist` and `node_modules` directories
git clean -fdx
npm install
npm publish
```
