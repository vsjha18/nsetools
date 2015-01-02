import os
from setuptools import setup, find_packages

readme = 'sample readme'

setup(
    name="nsetools",
    version="0.2.0",
    author="Vivek Jha",
    author_email="vsjha18@gmail.com",
    description = ("Python library for extracting realtime data from National Stock Exchange"),
    license="MIT",
    keywords="nse quote market",
    url ="http://vsjha18.github.com/nsetools",
    packages = find_packages(),
    long_description=readme,
)

