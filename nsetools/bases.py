"""
    The MIT License (MIT)

    Copyright (c) 2014 Vivek Jha

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

from abc import ABCMeta, abstractmethod
import six


class AbstractBaseExchange(six.with_metaclass(ABCMeta, object)):

    @abstractmethod
    def get_stock_codes(self):
        """
        :return: list of tuples with stock code and stock name
        """
        raise NotImplementedError

    @abstractmethod
    def is_valid_code(self, code):
        """
        :return: True, if it is a valid stock code, else False
        """
        raise NotImplementedError

    @abstractmethod
    def get_quote(self, code):
        """
        :param code: a stock code
        :return: a dictionary which contain detailed stock code.
        """
        raise NotImplementedError

    @abstractmethod
    def get_top_gainers(self):
        """
        :return: a sorted list of codes of top gainers
        """
        raise NotImplementedError

    @abstractmethod
    def get_top_losers(self):
        """
        :return: a sorted list of codes of top losers
        """
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        """
        :return: market name
        """
        raise NotImplementedError
