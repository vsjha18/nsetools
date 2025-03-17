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
        """Initialize a new NSE object.
        Initializes a session management for making API calls to NSE (National Stock Exchange).
        Args:
            session_refresh_interval (int, optional): Time interval in seconds after which the session 
                should be refreshed. Defaults to 120 seconds.
        Note:
            The session refresh interval helps maintain an active connection with NSE servers by
            periodically creating a new session to prevent timeouts.
        """
        
        self.session_refresh_interval = session_refresh_interval 
        self.session = Session(session_refresh_interval)

    #############################
    ###      STOCKS APIS      ###
    #############################
    
    def get_stock_codes(self):
        """Gets a list of stock codes traded in NSE.

        This function fetches stock data from NSE's CSV endpoint and extracts the stock symbols.

        Returns:
            list: A list of strings containing stock symbols traded on NSE.

        Example:
            >>> nse = Nse()
            >>> codes = nse.get_stock_codes()
            >>> print(codes[:5])
            ['20MICRONS', '3IINFOTECH', '3MINDIA', '3PLAND', '63MOONS']
        """
        res = self.session.fetch(urls.STOCKS_CSV_URL)
        csv_content = res.text.splitlines()
        symbols = []
        csv_reader = csv.DictReader(csv_content)
        for row in csv_reader:
            symbols.append(row['SYMBOL'])
        return symbols

    def is_valid_code(self, code):
        """Checks if a given stock code is valid.

        This method validates whether the provided stock code exists in the list of valid
        stock codes from NSE (National Stock Exchange).

        Args:
            code (str): Stock code/symbol to validate.

        Returns:
            bool: True if the code is valid, False otherwise.

        Example:
            >>> nse = NSE()
            >>> nse.is_valid_code("INFY")
            True
            >>> nse.is_valid_code("INVALID")
            False
        """
        stock_codes = self.get_stock_codes()
        return code.upper() in stock_codes

    def get_quote(self, code, all_data=False):
        """Gets the stock quote for a given NSE stock symbol.

        This function fetches real-time or delayed quote data from NSE for the specified stock code.

        Args:
            code (str): NSE stock symbol/code for which quote is to be fetched
            all_data (bool, optional): If True returns complete quote data, if False returns only price info. 
            Defaults to False.

        Returns:
            dict: A dictionary containing quote data.

        Raises:
            requests.exceptions.RequestException: If there is an error in HTTP request
            ValueError: If the response JSON is invalid

        Example:
            >>> nse = Nse()
            >>> nse.get_quote('abb')
            {
            'lastPrice': 5189.1,
            'change': 70.55,
            'pChange': 1.38,
            'previousClose': 5118.55,
            'open': 5160,
            'close': 5187.65,
            'vwap': 5162.91,
            'stockIndClosePrice': 0,
            'lowerCP': 4606.7,
            'upperCP': 5630.4,
            'pPriceBand': 'No Band',
            'basePrice': 5118.55,
            'intraDayHighLow': {'min': 5101, 'max': 5218.45, 'value': 5189.1},
            'weekHighLow': {'min': 4890}
            }
        """
        code = code.upper()
        # TODO: implement if the code is valid
        res = self.session.fetch(urls.QUOTE_API_URL % code)
        res = res.json()['priceInfo'] if all_data is False else res.json()
        return cast_intfloat_string_values_to_intfloat(res)
    
    def get_52_week_high(self):
        """Retrieves a list of stocks that have hit their 52-week high.

        This method fetches data for stocks that have reached new 52-week high prices on the NSE.

        Returns:
            list[dict]: A list of dictionaries containing 52-week high data.

        Example:
            >>> nse.get_52_week_high()
            [{'symbol': 'AVANTIFEED',
              'series': 'EQ', 
              'comapnyName': 'Avanti Feeds Limited',
              'new52WHL': 899,
              'prev52WHL': 849.9,
              'prevHLDate': '13-Mar-2025',
              'ltp': 887,
              'prevClose': 842.55,
              'change': 44.45,
              'pChange': 5.28},
                {...}
            ]
        """
        res = self.session.fetch(urls.FIFTYTWO_WEEK_HIGH_URL)
        return cast_intfloat_string_values_to_intfloat(res.json())['data']
    
    def get_52_week_low(self):
        """Retrieves a list of stocks that have hit their 52-week low.

        This method fetches data for stocks that have reached new 52-week low prices on the NSE.

        Returns:
            list[dict]: A list of dictionaries containing 52-week low data.

        Example:
            >>> nse.get_52_week_low()
            [{'symbol': 'AVANTIFEED',
              'series': 'EQ', 
              'comapnyName': 'Avanti Feeds Limited',
              'new52WHL': 899,
              'prev52WHL': 849.9,
              'prevHLDate': '13-Mar-2025',
              'ltp': 887,
              'prevClose': 842.55,
              'change': 44.45,
              'pChange': 5.28},
                {...}
            ]
        """
        res = self.session.fetch(urls.FIFTYTWO_WEEK_LOW_URL)
        return cast_intfloat_string_values_to_intfloat(res.json())['data']
    
    #############################
    ###       INDEX APIS      ###
    #############################
    
    def get_index_quote(self, index="NIFTY 50"):
        """Gets the quote for a specific index from NSE.

        This function retrieves detailed quote information for a given index code from the
        National Stock Exchange (NSE) of India.

        Args:
            index (str): The index code/symbol (e.g. "NIFTY 50", "BANKNIFTY", etc.)

        Returns:
            dict: A dictionary containing index quote details

        Raises:
            Exception: If the provided index code is invalid or not found

        Example:
            >>> nse = NSE()
            >>> nse.get_index_quote("NIFTY 50")
            {
            'key': 'BROAD MARKET INDICES',
            'index': 'NIFTY 50', 
            'last': 22508.75,
            'variation': 111.55,
            'percentChange': 0.5,
            'open': 22353.15,
            'high': 22577.0,
            'low': 22353.15,
            'previousClose': 22397.2,
            'yearHigh': 26277.35,
            'yearLow': 21281.45,
            # ... additional fields omitted for brevity
            }
        """
        
        url = urls.ALL_INDICES_URL
        all_index_quote = self.get_all_index_quote()
        index_list = [ i['indexSymbol'] for i in all_index_quote]
        index = index.upper()
        index = ' '.join(index.split())
        if index in index_list:
            response = list(filter(lambda idx: idx['indexSymbol'] == index, all_index_quote))[0]
            return cast_intfloat_string_values_to_intfloat(response)
        else:
            raise Exception('Wrong index code')
    
    def get_index_list(self):
        """Gets a list of all NSE index symbols.

        This method fetches all available NSE (National Stock Exchange) index symbols by
        extracting the 'indexSymbol' from the complete index quote data.

        Returns:
            list: A list of strings containing index symbols (e.g., ['NIFTY 50', 'NIFTY BANK', ...])

        Examples:
            >>> nse = Nse()
            >>> indices = nse.get_index_list()
            >>> print(indices)
            ['NIFTY 50', 'NIFTY BANK', 'NIFTY IT', ...]
        """
        return [ i['indexSymbol'] for i in self.get_all_index_quote()]
    
    def get_all_index_quote(self):
        """Gets information for all NSE indices in one request.

        This method fetches quotes and information for all available indices on the
        National Stock Exchange (NSE) through a single API call.

        Returns:
            list[dict]: A list of dictionaries where each dictionary contains quote
            information for an index. The quote information includes details like
            index name, current value, change, percentage change etc.

        Example:
            >>> nse = Nse()
            >>> quotes = nse.get_all_index_quote()
            >>> quotes  # Sample output
            [
                {
                'key': 'BROAD MARKET INDICES',
                'index': 'NIFTY 50',
                'indexSymbol': 'NIFTY 50', 
                'last': 22508.75,
                'variation': 111.55,
                'percentChange': 0.5,
                'open': 22353.15,
                ...
                },
                # ... additional indices follow
            ]

        Raises:
            URLError: If there is an error accessing the NSE API endpoint
            ValueError: If the response JSON cannot be parsed properly
        """
        url = urls.ALL_INDICES_URL
        res = self.session.fetch(url)
        return res.json()['data']
    
    def get_top_gainers(self, index="NIFTY"):
        """Gets the list of top gaining stocks for the specified index.

        This function retrieves real-time data for stocks that have gained the most value
        during the current trading day. It can filter results by different indices.

        Args:
            index (str, optional): The index to get top gainers for. Defaults to "NIFTY".
            Valid values are:
            - NIFTY: Nifty 50 index
            - BANKNIFTY: Bank Nifty index 
            - NIFTYNEXT50: Nifty Next 50 index
            - SecGtr20: Securities greater than 20 
            - SecLwr20: Securities lower than 20
            - FNO: Futures & Options
            - ALL: All stocks

        Returns:
            list[dict]: List of dictionaries containing top gainer details.
            
        Raises:
            ConnectionError: If unable to fetch data from NSE
            
        Example:
            >>> nse = Nse()
            >>> gainers = nse.get_top_gainers()
            >>> gainers[0]  # Sample output
            {
            'symbol': 'DRREDDY',
            'series': 'EQ',
            'open_price': 1107.9,
            'high_price': 1154.1,
            'low_price': 1101.5,
            'ltp': 1151.5,
            'prev_price': 1107.95,
            'net_price': 3.93,
            'trade_quantity': 2714559,
            'turnover': 31016.01,
            'market_type': 'N',
            'ca_ex_dt': '28-Oct-2024',
            'ca_purpose': 'Face Value Split (Sub-Division) - From Rs 5/- Per Share To Re 1/- Per Share',
            'perChange': 3.93
            }
        """
        return self._get_top_gainers_losers('gainers', index)

    def get_top_losers(self, index="NIFTY"):  # Changed from None to "NIFTY"
        """Gets the top losers from specified index from NSE.

        The function fetches real-time data for stocks that have declined the most in terms
        of percentage change compared to their previous closing price.

        Args:
            index (str, optional): Index name for which top losers are to be fetched.
                Available options:
                    - NIFTY (Default)
                    - BANKNIFTY
                    - NIFTYNEXT50  
                    - SecGtr20
                    - SecLwr20
                    - FNO
                    - ALL

        Returns:
            list: List of dictionaries containing stock information with following keys:
        
        Raises:
            URLError: When unable to connect to NSE
            ValueError: When invalid index is provided

        Examples:
            >>> from nsetools import Nse
            >>> nse = Nse()
            >>> losers = nse.get_top_losers()
            >>> losers[0]
            {'symbol': 'TATAMOTORS', 'series': 'EQ', 'openPrice': 375.0, ...}
        """
        return self._get_top_gainers_losers('losers', index)  # Changed from 'gainers' to 'losers'
    
    def get_advances_declines(self, index='nifty 50'):
        """Gets the advances/declines data for given index.
        This method provides the number of stocks advancing and declining in a given index
        on NSE at any given point of time.
        Args:
            index (str, optional): Name of the index. Defaults to 'nifty 50'.
                Valid values include 'NIFTY 50', 'NIFTY BANK', etc.
        Returns:
            dict: A dictionary with two keys:
                - 'advances': Number of advancing stocks in the index
                - 'declines': Number of declining stocks in the index
        Examples:
            >>> nse = Nse()
            >>> nse.get_advances_declines(index="NIFTY BANK")
            {'advances': 7, 'declines': 4}
        Note:
            The method is case-insensitive for the index parameter.
        """
        
        # fixing this
        index = index.upper()
        index_quote = self.get_index_quote(index)
        return {'advances': index_quote['advances'], 'declines': index_quote['declines']}
    
    def get_stocks_in_index(self, index="NIFTY 50"):
        """Gets the list of symbols of stocks included in the specified NSE index.
        The function retrieves the current constituents of a given NSE index like NIFTY 50, 
        NIFTY BANK etc. and returns their stock symbols.
        Args:
            index (str, optional): Name of the NSE index. Defaults to "NIFTY 50".
                Possible values: "NIFTY 50", "NIFTY BANK", "NIFTY IT" etc.
        Returns:
            list: List of stock symbols (str) that are part of the specified index.
        Raises:
            URLError: If unable to connect to NSE server
            ValueError: If invalid index name is provided
        Examples:
            >>> nse = Nse()
            >>> nse.get_stocks_in_index("NIFTY 50")
            ['ADANIPORTS', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', ...]
            >>> nse.get_stocks_in_index("NIFTY BANK") 
            ['AUBANK', 'AXISBANK', 'BANDHANBNK', 'FEDERALBNK', 'HDFCBANK', ...]
        """
        
        index = index.upper()
        url = urls.STOCKS_IN_INDEX_URL % index
        res = self.session.fetch(url)
        res_dict = res.json()
        return  [stock['symbol'] for stock in res_dict['data']][1:]
    
    def get_stock_quote_in_index(self, index="NIFTY 50", include_index=False):
        """Gets stock quotes for all stocks in a given index.
        This function fetches real-time quotes for all stocks that are part of the specified index
        from NSE (National Stock Exchange).
        Args:
            index (str, optional): The name of the index. Defaults to "NIFTY 50".
            include_index (bool, optional): Whether to include the index itself in results.
                If True, includes both stocks and index. If False, returns only stocks.
                Defaults to False.
        Returns:
            list: A list of dictionaries containing stock quote data.
                Each dictionary contains various fields including:
                - symbol: Stock symbol
                - open: Opening price
                - high: High price
                - low: Low price
                - lastPrice: Last traded price
                - change: Change in price
                - pChange: Percentage change
                And other relevant trading information.
        Raises:
            URLError: If unable to connect to NSE servers
            ValueError: If invalid index name is provided
        Example:
            >>> nse = Nse()
            >>> nifty_quotes = nse.get_stock_quote_in_index("NIFTY 50")
            >>> nifty_quotes_with_index = nse.get_stock_quote_in_index("NIFTY 50", include_index=True)
        """
        
        index = index.upper()
        url = urls.STOCKS_IN_INDEX_URL % index
        res = self.session.fetch(url)
        res_dict = res.json()
        res_dict = cast_intfloat_string_values_to_intfloat(res_dict)
        if include_index is False:
            return  [record for record in res_dict['data'] if record['priority'] == 0]
        else:
            return res_dict['data']

    def _get_top_gainers_losers(self, direction, index):
        """Internal method to fetch top gainers or losers for a given index.

        Args:
            direction (str): Either 'gainers' or 'losers'
            index (str): Index name - one of NIFTY, BANKNIFTY, NIFTYNEXT50, SecGtr20, SecLwr20, FNO, ALL

        Returns:
            list: List of dictionaries containing top gainers/losers data for the specified index

        Raises:
            ValueError: If invalid index name is provided
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
        """Get future quote for given stock code.

        This function fetches futures trading data for a given stock code from NSE's derivatives segment.
        If expiry date is provided, returns data for that specific expiry, else returns data for all
        available expiry dates.

        Args:
            code (str): Stock code for which futures data needs to be fetched
            expiry_date (str, optional): Expiry date in format DD-MMM-YYYY (e.g. "27-Mar-2025"). 
                           Defaults to None.

        Returns:
            Union[dict, list]: If expiry_date provided returns dict with futures data for that expiry,
                      else returns list of dicts with data for all expiries.

        Example:
            >>> nse = Nse()
            >>> nse.get_future_quote('RELIANCE') 
            [{'expiryDate': '27-Mar-2025',
              'lastPrice': 1246,
              'premium': 4.45,
              'openPrice': 1245.25,
              'highPrice': 1260.85,
              'lowPrice': 1236.2,
              'openInterest': 257812,
              'changeInOpenInterest': 7144,
              ...},
             {...}]
        """

        url = urls.QUOTE_DRIVATIVE_URL % code.upper()
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
        """Returns a string representation of the NSE driver class.
        Returns:
            str: A descriptive string identifying this as the NSE driver class.
        """
        
        return 'Driver Class for National Stock Exchange (NSE)'


if __name__ == "__main__":
    n = Nse()
    # data = n.download_bhavcopy("14th Dec")
    n.get_quote('reliance')
