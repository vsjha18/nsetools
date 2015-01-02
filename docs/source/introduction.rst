Introduction
============

nsetools is a library for collecting real time data from National Stock Exchange (India).
It can be used in various types of projects which requires fetching live quotes for a given
stock or index or building large data sets for further data analytics. You can also build cli
applications which can provide you live market details at a blazing fast speeds, much faster
than any browser. The accuracy of data is only as correct as provided on `www.nseindia.com`_

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

Installing nsetools is very simple and it has no external dependencies. All its dependencies
are part of standard python distribution. 
packages::

    pip install nsetools


Python 3 Support
================

It doesn't support python 3 at the moment. If you want it to work in python3, then get ready 
to get your hands dirty. Please clone the source code and invoke the python2to3 converter 
script. Run the unittests to verify if everything still works properly. Unittest has cent 
percent branch and api coverage.

A Word On Exception Handling 
============================

Since this library would form a middleware of some other project. Hence it is not handling any 
exception. Apart from standard python exceptions, you should be catching the following two:

    * URLError
    * HTTPError 

Both of them can be imported from **urllib2**.


.. warning::

    You need to have a working internet connection while using this library. It will raise URLErorr 
    in case there is no internet connectivity. Hence please handle this scenario in your code.


