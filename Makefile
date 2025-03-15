# Makefile for running tests

# Python executable and pytest command
PYTHON = python3
PYTEST = pytest

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "NSETools Makefile commands:"
	@echo "-------------------------"
	@echo "make dev       : Install all development dependencies"
	@echo "make test      : Run tests with coverage report in terminal"
	@echo "make cov       : Generate coverage XML report"
	@echo "make clean     : Remove Python cache files"
	@echo "make pristine  : Remove all installed packages from virtualenv"
	@echo "make build     : Build the package"
	@echo "-------------------------"

# Install packages for development
dev:
	pip install --upgrade pip
	pip install ipython pytest pytest-cov build setuptools wheel twine
	pip install -e .

# Target to run the tests
test:
	$(PYTEST) --cov=nsetools --cov-report=term -v

cov:
	$(PYTEST) --cov=nsetools --cov-report=xml -v

# Clean up pycache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +

# Remove all installed packages in the venv (pristine)
pristine:
	pip list --disable-pip-version-check | awk 'NR>2 {print $$1}' | grep -v "^pip$$" | xargs -r pip uninstall -y

build:
	python -m build

