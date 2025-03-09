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

import requests
import csv
from datetime import datetime as dt 
from nsetools.bases import AbstractBaseExchange
from nsetools import urls
from nsetools.ua import Session
from nsetools.utils import cast_intfloat_string_values_to_intfloat

class Nse(AbstractBaseExchange):
    """
    class which implements all the functionality for
    National Stock Exchange
    """
    __CODECACHE__ = None

    def __init__(self, session_refresh_interval=120):
        self.session_refresh_interval = session_refresh_interval 
        self.session = Session(session_refresh_interval)
    
    def get_stock_codes(self):
        """ returns a list of stock codes traded in NSE
        :return: list
        """
        res = self.session.fetch(urls.STOCKS_CSV_URL)
        csv_content = res.text.splitlines()
        symbols = []
        csv_reader = csv.DictReader(csv_content)
        for row in csv_reader:
            symbols.append(row['SYMBOL'])
        return symbols

    def is_valid_code(self, code):
        """
        :param code: a string stock code
        :return: Boolean
        """
        stock_codes = self.get_stock_codes()
        return code.upper() in stock_codes

    def get_quote(self, code, all_data=False):
        """
        gets the quote for a given stock code
        :param code:
        :return: dict or None
        :raises: HTTPError
        """
        code = code.upper()
        # TODO: implement if the code is valid
        res = self.session.fetch(urls.QUOTE_API_URL % code)
        res = res.json()['priceInfo'] if all_data is False else res.json()
        return cast_intfloat_string_values_to_intfloat(res)
    
    def get_top_gainers(self, index=None):
        """
        :return: a list of dictionaries containing top gainers of the day for all indices
        """
        url = urls.TOP_GAINERS_URL
        res = self.session.fetch(url)
        res_dict = res.json()
        if index is None:
            return cast_intfloat_string_values_to_intfloat(res_dict)
        else:
            res_dict = res_dict[index]
            return res_dict['data']


    def get_top_losers(self, index=None):
        """
        :return: a list of dictionaries containing top losers of the day for all indices
        """
        url = urls.TOP_LOSERS_URL
        res = self.session.fetch(url)
        res_dict = res.json()
        if index is None:
            return cast_intfloat_string_values_to_intfloat(res_dict)
        else:
            res_dict = res_dict[index]
            return res_dict['data']
    
    def get_advances_declines(self, code='nifty 50'):
        """
        :return: a list of dictionaries with advance decline data
        :raises: URLError, HTTPError
        """
        # fixing this
        code = code.upper()
        index_quote = self.get_index_quote(code)
        return {'advances': index_quote['advances'], 'declines': index_quote['declines']}
        
    

    def get_index_list(self):
        """ get list of indices and codes
        returns: a list | json of index codes
        """
        return [ i['indexSymbol'] for i in self.get_all_index_quote()]
    
    def get_index_quote(self, code):
        """
        params:
            code : string index code
        returns:
            dict 
        """
        url = urls.ALL_INDICES_URL
        all_index_quote = self.get_all_index_quote()
        index_list = [ i['indexSymbol'] for i in all_index_quote]
        code = code.upper()
        code = ' '.join(code.split())
        if code in index_list:
            response = list(filter(lambda idx: idx['indexSymbol'] == code, all_index_quote))[0]
            return cast_intfloat_string_values_to_intfloat(response)
        else:
            raise Exception('Wrong index code')
    
    def get_all_index_quote(self):
        """
        Gets information of all indices and one go
        returns:
            list of dicts
        """
        url = urls.ALL_INDICES_URL
        res = self.session.fetch(url)
        return res.json()['data']

    def __str__(self):
        """
        string representation of object
        :return: string
        """
        return 'Driver Class for National Stock Exchange (NSE)'


if __name__ == "__main__":
    n = Nse()
    # data = n.download_bhavcopy("14th Dec")
    n.get_quote('reliance')
