# Makefile for running tests

# Python executable and pytest command
PYTHON = python3
PYTEST = pytest

# Target to run the tests
test:
	$(PYTEST) --cov=nsetools --cov-report=term -v

cov:
	$(PYTEST) --cov=nsetools --cov-report=xml -v

# Clean up pycache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +

# Remove all installed packages in the venv (pristine)
pristine:
	$(PYTHON) -m pip freeze | xargs $(PYTHON) -m pip uninstall -y

# Install dependencies from requirements.txt
install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

