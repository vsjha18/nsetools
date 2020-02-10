from setuptools import setup, find_packages

readme = '''
Project Page
=================
http://nsetools.readthedocs.io

nsetools
=================
Python library for extracting realtime data from National Stock Exchange (India)

Introduction.
=================
nsetools is a library for collecting real time data from National Stock Exchange (India). It can be used in various types of projects which requires getting live quotes for a given stock or index or build large data sets for further data analytics. You can also build cli applications which can provide you live market details at a blazing fast speeds, much faster that the browsers. The accuracy of data is only as correct as provided on www.nseindia.com.

Main Features:
==================

    * Getting live quotes for stocks using stock codes.
    * Return data in both json and python dict and list formats.
    * Getting quotes for all the indices traded in NSE, e.g CNX NIFTY, BANKNIFTY
    * etc.
    * Getting list of top losers.
    * Getting list of top gainers.
    * Helper APIs to check whether a given stock code or index code is correct.
    * Getting list of all indices and stocks.
    * Cent percent unittest coverage.

Dependencies
===================
To keep it simple and supported on most of the platforms, it uses only core python libraries, hence there are no external dependencies. It can be used out of box and absolutely not set up is required except an internet connection.

Detailed Documenation
========================
For complete documenation, please refer http://nsetools.readthedocs.io
'''

setup(
    name="nsetools",
    version="1.0.11",
    author="Vivek Jha",
    author_email="vsjha18@gmail.com",
    description="Python library for extracting realtime data from National Stock Exchange",
    license="MIT",
    keywords="nse quote market",
    install_requires=['six', 'dateutils'],
    url="http://vsjha18.github.com/nsetools",
    packages=find_packages(),
    long_description=readme,
)
