Introduction
============

nsetools is a library for collecting real time data from National Stock Exchange (India).
It can be used in various types of projects which requires getting live quotes for a given
stock or index or build large data sets for further data analytics. You can also build cli
applications which can provide you live market details at a blazing fast speeds, much faster
that the browsers. The accuracy of data is only as correct as provided on `www.nseindia.com`_

.. note:: 
    The data provided by APIs is only as correct as provided on www.nseindia.com

 .. _`www.nseindia.com`: www.nseindia.com

Main Features
=============

    #. Works out of box, without any required setup.
    #. Fetches live stock code and index codes in blazing fast speed.
    #. Provides list of all indices and stocks traded in National Stock Exchange.
    #. Additionally provides list of:
        * Top losers.
        * Top gainers.
        * Most active.
    #. Provides some useful APIs to validate a stock code and index code.
    #. Optionally returns data in JSON format.
    #. Hunderd Percent Unittest coverage.

Installation
============

Installing nsetools is very simple and it has been delibrating written in such a way 
so that it doesn't have any additional dependencies apart from standard python 
packages::

    pip install nsetools




