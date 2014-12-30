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

from urllib2 import build_opener, HTTPCookieProcessor, Request
from urllib import urlencode
from cookielib import CookieJar
import ast
from nselib.bases import AbstractBaseExchange
import re
import json

class Nse(AbstractBaseExchange):
    """
    class which implements all the functionality for
    National Stock Exchange
    """
    __CODECACHE__ = None

    def __init__(self):
        self.opener = self.nse_opener()
        self.headers = self.nse_headers()
        # URL list
        self.get_quote_url = 'http://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?'
        self.stocks_csv_url = 'http://www.nseindia.com/content/equities/EQUITY_L.csv'
        self.top_gainer_url = 'http://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json'
        self.top_loser_url = 'http://www.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json'
        self.advances_declines_url = 'http://www.nseindia.com/common/json/indicesAdvanceDeclines.json'
        self.index_url="http://www.nseindia.com/homepage/Indices1.json"

    def get_stock_codes(self, cached=True):
        """
        returns a dictionary with key as stock code and value as stock name.
        It also implements cache functionality and hits the server only
        if user insists or cache is empty
        :return: dict
        """
        url = self.stocks_csv_url
        req = Request(url, None, self.headers)
        res_dict = {}
        if cached is not True or self.__CODECACHE__ is None:
            # raises HTTPError and URLError
            res = self.opener.open(req)
            if res is not None:
                for line in res.read().split('\n'):
                    if line != '' and re.search(',', line):
                        (code, name) = line.split(',')[0:2]
                        res_dict[code] = name
                    # else just skip the evaluation, line may not be a valid csv
            else:
                raise Exception('no response received')
            self.__CODECACHE__ = res_dict
        return self.__CODECACHE__

    def is_valid_code(self, code):
        """
        :param code: a string stock code
        :return: Boolean
        """
        if code:
            stock_codes = self.get_stock_codes()
            if code.upper() in stock_codes.keys():
                return True
            else:
                return False

    def get_quote(self, code):
        """
        gets the quote for a given stock code
        :param code:
        :return: dict or None
        :raises: HTTPError, URLError
        """
        if self.is_valid_code(code):
            url = self.build_url_for_quote(code)
            req = Request(url, None, self.headers)
            # this can raise HTTPError and URLError, but we are not handling it
            # north bound APIs should use it for exception handling
            res = self.opener.open(req)

            # Now parse the response to get the relevant data
            match = re.search(\
                        r'\{<div\s+id="responseDiv"\s+style="display:none">\s+(\{.*?\{.*?\}.*?\})',
                        res.read(), re.S
                    )
            # ast can raise SyntaxError, let's catch only this error
            try:
                return self.clean_server_response(ast.literal_eval(match.group(1))['data'][0])
            except SyntaxError as err:
                raise Exception('ill formatted response')
        else:
            return None

    def get_top_gainers(self):
        """
        :return: a list of dictionaries containing top gainers of the day
        """
        url = self.top_gainer_url
        req = Request(url, None, self.headers)
        # this can raise HTTPError and URLError
        res = self.opener.open(req)
        res_dict = json.load(res)
        # clean the output and make appropriate type conversions
        res_list = [self.clean_server_response(item) for item in res_dict['data']]
        return res_list

    def get_top_losers(self):
        """
        :return: a list of dictionaries containing top losers of the day
        """
        url = self.top_loser_url
        req = Request(url, None, self.headers)
        # this can raise HTTPError and URLError
        res = self.opener.open(req)
        res_dict = json.load(res)
        # clean the output and make appropriate type conversions
        res_list = [self.clean_server_response(item)
                    for item in res_dict['data']]
        return res_list

    def get_advances_declines(self, ret_type='dict'):
        """
        :return: a list of dictionaries with advance decline data
        :raises: URLError, HTTPError
        """
        url = self.advances_declines_url
        req = Request(url, None, self.headers)
        # raises URLError or HTTPError
        resp = self.opener.open(req)
        resp_dict = json.load(resp)
        resp_list = [self.clean_server_response(item)
                     for item in resp_dict['data']]
        return self.render_response(ret_type, resp_list)

    def is_valid_index(self, code):
        url = self.index_url
        req = Request(url, None, self.headers)
        # raises URLError or HTTPError
        resp = self.opener.open(req)
        resp_list = json.load(resp)['data']
        # extract index codes from the above response
        index_list = [str(item['name']) for item in resp_list]
        return True if code.upper() in index_list else False

    def get_index_quote(self, code, ret_type='dict'):
        url = self.index_url
        if self.is_valid_index(code):
            req = Request(url, None, self.headers)
            # raises HTTPError and URLError
            resp = self.opener.open(req)
            resp_list = json.load(resp)['data']
            # this is list of dictionaries
            resp_list = [self.clean_server_response(item)
                         for item in resp_list]
            # search the right list element to return
            search_flag = False
            for item in resp_list:
                if item['name'] == code.upper():
                    search_flag = True
                    break
            return self.render_response(ret_type, item) if search_flag else None
    def nse_headers(self):
        """
        Builds right set of headers for requesting http://nseindia.com
        :return: a dict with http headers
        """
        return {'Accept' : '*/*',
                'Accept-Language' : 'en-US,en;q=0.5',
                'Host': 'nseindia.com',
                'Referer': 'http://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=INFY&illiquid=0',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
                'X-Requested-With': 'XMLHttpRequest'
            }

    def nse_opener(self):
        """
        builds opener for urllib2
        :return: opener object
        """
        cj = CookieJar()
        return build_opener(HTTPCookieProcessor(cj))

    def build_url_for_quote(self, code):
        """
        builds a url which can be requested for a given stock code
        :param code: string containing stock code.
        :return: a url object
        """
        if code is not None and type(code) is str:
            encoded_args = urlencode({'symbol':code, 'illiquid':'0'})
            return self.get_quote_url + encoded_args
        else:
            raise Exception('code must be string')

    def clean_server_response(self, resp_dict):
        """
        cleans the server reponse by replacing:
            '-'     -> None
            '1,000' -> 1000
        :param resp_dict:
        :return: dict with all above substitution
        """
        # change all the keys from unicode to string
        d = {}
        for key, value in resp_dict.iteritems():
            d[str(key)] = value
        resp_dict = d
        for key, value in resp_dict.iteritems():
            if type(value) is str or type(value) is unicode:
                if re.match('-', value):
                    resp_dict[key] = None
                elif re.search(r'^[0-9,.]+$', value):
                    # replace , to '', and type cast to int
                    resp_dict[key] = float(re.sub(',', '', value))
                else:
                    resp_dict[key] = str(value)
        return resp_dict

    def render_response(self, ret_type, data):
        if ret_type == 'json':
            return json.dumps(data)
        elif ret_type == 'dict':
            return data
        else:
            raise Exception("only 'dict' and 'json' return types are supported")

    def __str__(self):
        """
        string representation of object
        :return: string
        """
        return 'Driver Class for National Stock Exchange (NSE)'

if __name__ == '__main__':
    nse = Nse()
    import json
    print nse.get_index_quote('cnx nifty')
    print nse.get_index_quote('cnx nifty', ret_type='json')
    print nse.get_index_quote('cx nifty')

    # print json.dumps(nse.get_quote('INFY'))
    # TODO: get_indices
    # TODO: get_index_quote(index)
    # TODO: Implement different return formats in network APIs
    # TODO: get_most_active()
    # TODO: get_top_volume()
    # TODO: get_peer_companies()
    # TODO: is_market_open()
    # TODO: get_advance_declines()
    # TODO: concept of portfolio for fetching price in a batch and field which should be captured
    # TODO: Concept of session, just like as in sqlalchemy
