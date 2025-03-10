# Commands 

## Setup Dev Environment 

```
pip install ipdb ipython pytest pytest-cov requests dateutils six 
```

> To see coverage install covergae gutters extension and follow Makefile

### Run Tests 

```bash
cd $VIRTUAL_ENV/nsetools
pytest --cov=nsetools --cov-report=term -v
# or if are specific on a test module
pytest --cov=nsetools --cov-report=term tests/test_session.py -v
```

## Test Build Locally 

Make a new virtual env, if using existing virtual env remove all extensions on each iteration using this command and use the next command to install the package from path

```bash
pip freeze | xargs pip uninstall -y
pip install /path/to/your/package.whl
OR
pip install /path/to/your/package.tar.gz
```

## Publishing
Follow these instructions for building.

* move setup.py one level up.
* run command from there.
* change version in `setup.py` and `__init__.py`

```bash
pip install requests dateutils wheel twine setuptools
```

* Command to build 

```bash
python setup.py sdist bdist_wheel
```
* Command to upload

```bash
twine upload --username __token__ --password <API-TOKEN> dist/*
```
