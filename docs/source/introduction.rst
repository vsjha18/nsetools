Introduction
============

nsetools is a library for collecting real time data from National Stock Exchange (India).
It can be used in various types of projects which requires fetching live quotes for a given
stock or index or building large data sets for further data analytics. You can also build cli
applications which can provide you live market details at a blazing fast speeds, much faster
than any browser. The accuracy of data is only as correct as provided on http://www.nseindia.com


.. note:: 
    The data provided by APIs is only as correct as provided on http://www.nseindia.com


Github Project Page
===================

https://github.com/vsjha18/nsetools


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

Update
===============

To updated to the lasted version::

    pip install nsetools --upgrade

Python 3 Support
================

Python 3 support has been added from 1.0.0 and onwards. Python 2 support was removed in
1.0.3.

A Word On Exception Handling 
============================

Since this library would form a middleware of some other project. Hence it is not handling any 
exception. Apart from standard python exceptions, you should be catching the following two:

    * URLError
    * HTTPError 

.. warning::

    You need to have a working internet connection while using this library. It will raise URLErorr 
    in case there is no internet connectivity. Hence please handle this scenario in your code.

.. warning::

    If you are facing any issue with the APIs then it may be beacuse there had been some format 
    change recently in the way NSE reports its live quotes. Please upgrade to the latest version 
    in order to avoid this issue.

.. warning::

    Now nsetools doesn't support python 2 officially, though it may still continue to work with 
    python 2 for some more time.

.. disqus::


