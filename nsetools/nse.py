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

    #############################
    ###      STOCKS APIS      ###
    #############################
    
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
    
    def get_52_week_high(self):
        """
        :return: list of dictionaries containing stocks on 52 week high data
        """
        res = self.session.fetch(urls.FIFTYTWO_WEEK_HIGH_URL)
        return cast_intfloat_string_values_to_intfloat(res.json())['data']
    
    def get_52_week_low(self):
        """
        :return: list of dictionaries containing stocks on 52 week low data
        """
        res = self.session.fetch(urls.FIFTYTWO_WEEK_LOW_URL)
        return cast_intfloat_string_values_to_intfloat(res.json())['data']
    
    #############################
    ###       INDEX APIS      ###
    #############################
    
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
    
    def get_index_list(self):
        """ get list of indices and codes
        returns: a list | json of index codes
        """
        return [ i['indexSymbol'] for i in self.get_all_index_quote()]
    
    def get_all_index_quote(self):
        """
        Gets information of all indices and one go
        returns:
            list of dicts
        """
        url = urls.ALL_INDICES_URL
        res = self.session.fetch(url)
        return res.json()['data']
    
    def get_top_gainers(self, index="NIFTY"):
        """
        :param index: one of NIFTY, BANKNIFTY, NIFTYNEXT50, SecGtr20, SecLwr20, FNO, ALL
        :return: a list of dictionaries containing top gainers of the day for all indices
        """
        return self._get_top_gainers_losers('gainers', index)

    def get_top_losers(self, index="NIFTY"):  # Changed from None to "NIFTY"
        """
        :param index: one of NIFTY, BANKNIFTY, NIFTYNEXT50, SecGtr20, SecLwr20, FNO, ALL
        :return: a list of dictionaries containing top losers of the day for all indices
        """
        return self._get_top_gainers_losers('losers', index)  # Changed from 'gainers' to 'losers'
    
    def get_advances_declines(self, code='nifty 50'):
        """
        :return: a list of dictionaries with advance decline data
        :raises: URLError, HTTPError
        """
        # fixing this
        code = code.upper()
        index_quote = self.get_index_quote(code)
        return {'advances': index_quote['advances'], 'declines': index_quote['declines']}
    
    def get_stocks_in_index(self, index="NIFTY 50"):
        """
        :param index: valid index name from api get_index_list
        :return: list of stock codes
        """
        index = index.upper()
        url = urls.STOCKS_IN_INDEX_URL % index
        res = self.session.fetch(url)
        res_dict = res.json()
        return  [stock['symbol'] for stock in res_dict['data']][1:]  

    def _get_top_gainers_losers(self, direction, index):
        """
        :param direction: one of gainers or losers
        :param index: one of NIFTY, BANKNIFTY, NIFTYNEXT50, SecGtr20, SecLwr20, FNO, ALL
        :return: a list of dictionaries containing top gainers or losers of the day for all indices
        IMP: This API has one abnormality that it actually takes NIFTY, BANKNIFTY, NIFTYNEXT50 etc.
        as index names, but these are not same as formal index symbols returned by get_index_list
        But I want users to have consistent experience hence I am mapping these formal ones to 
        the ones that this API expects. Since this API only supports six options, so it is possible
        map.
        """
        index = index or 'NIFTY'  # Default to NIFTY if None
        index = index.upper()
        index = {
            "NIFTY": "NIFTY",
            "NIFTY 50": "NIFTY",
            "NIFTY BANK": "BANKNIFTY",
            "BANKNIFTY": "BANKNIFTY",
            "NIFTYNEXT50": "NIFTYNEXT50",
            "NIFTY NEXT 50": "NIFTYNEXT50",
            "SECGTR20": "SecGtr20",
            "SECLWR20": "SecLwr20",
            "FNO": "FOSec",
            "ALL": "allSec"
        }.get(index)
        if index is None:
            raise ValueError("Index must be one of NIFTY 50, NIFTY BANK, NIFTY NEXT 50, SecGtr20, SecLwr20, FNO, ALL")
        url = urls.TOP_GAINERS_URL if direction == 'gainers' else urls.TOP_LOSERS_URL
        res = self.session.fetch(url)
        return cast_intfloat_string_values_to_intfloat(res.json())[index]['data']

    #############################
    ###    DERIVATIVE APIS    ###
    #############################

    def get_future_quote(self, code, expiry_date=None):
        """
        :param code: stock code
        :return: dict
        """
        url = urls.QUOTE_DRIVATIVE_URL % code
        res = self.session.fetch(url)
        res_dict = res.json()
        # list containing all options and futures data
        data = res_dict['stocks']
        # filter out only future data
        future_data = [s for s in data if s['metadata']['instrumentType'] == "Stock Futures"]
        # future data is very convoluted, so flatten-out the desired data
        # !! there is bug in spelling of the key 'dailyvolatility', it is not camel cased
        # fixing that in my code for uniformity
        filtered_data = [
            {
                'expiryDate': record['metadata']['expiryDate'],
                'lastPrice': record['metadata']['lastPrice'],
                'premium': record['metadata']['lastPrice'] - record['underlyingValue'],
                'openPrice': record['metadata']['openPrice'],
                'highPrice': record['metadata']['highPrice'],
                'lowPrice': record['metadata']['lowPrice'],
                'closePrice': record['metadata']['closePrice'],
                'prevClose': record['metadata']['prevClose'],
                'change': record['metadata']['change'],
                'pChange': record['metadata']['pChange'],
                'numberOfContractsTraded': record['metadata']['numberOfContractsTraded'],
                'totalTurnover': record['metadata']['totalTurnover'],
                'underlyingValue': record['underlyingValue'],
                'tradedVolume': record['marketDeptOrderBook']['tradeInfo']['tradedVolume'],
                'openInterest': record['marketDeptOrderBook']['tradeInfo']['openInterest'],
                'changeInOpenInterest': record['marketDeptOrderBook']['tradeInfo']['changeinOpenInterest'],
                'pchangeinOpenInterest': record['marketDeptOrderBook']['tradeInfo']['pchangeinOpenInterest'],
                'marketLot': record['marketDeptOrderBook']['tradeInfo']['marketLot'],
                'dailyVolatility': record['marketDeptOrderBook']['otherInfo']['dailyvolatility'],
                'annualisedVolatility': record['marketDeptOrderBook']['otherInfo']['annualisedVolatility']
            }
            for record in future_data
        ]
        # if expiry_date is provided, filter out data for that expiry date
        if expiry_date:
            # pick only the first record, there should be only one record for a given expiry date
            filtered_data = [record for record in filtered_data if record['expiryDate'] == expiry_date][0]
        return cast_intfloat_string_values_to_intfloat(filtered_data)
    
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
