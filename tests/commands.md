# Commands 

## Run Tests 
```bash
nosetests --with-coverage --cover-package nsetools.nse --cover-branch
python setup.py sdist upload -r pypi
```

## Test Locally 

* Install setuptools, wheel, twine will be needed for upload.
* `python setup.py bdist_wheel --verbose`
* Things will be found in the dist folder at the same level as setup tools.

Clean up the environment before installing the package.

```bash
pip uninstall -y certifi charset-normalizer dateutils idna nsetools python-dateutil pytz requests six urllib3
```

## Publishing
Follow these instructions for building.

* move setup.py one level up.
* run command from there.
* change version in `setup.py` and `__init__.py`
* Command to build 

```bash
python setup.py sdist bdist_wheel
```
* Command to upload

```bash
twine upload --username __token__ --password <API-TOKEN> dist/*
```
