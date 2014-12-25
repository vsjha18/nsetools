from urllib2 import build_opener, HTTPCookieProcessor, Request
from urllib import urlencode
from cookielib import CookieJar
import ast

from nselib.bases import AbstractBaseExchange
import re


class Nse(AbstractBaseExchange):
    """
        class which implements all the functionality for
        National Stock Exchange
    """
    def __init__(self):
        self.opener = self.nse_opener()
        self.headers = self.nse_headers()
        # URL list
        self.get_quote_url = 'http://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?'

    def is_open(self):
        pass

    def get_stock_codes(self):
        pass

    def is_valid_stock_code(self):
        pass

    def get_quote(self, code):
        """
        gets the quote for a given stock code
        :param code:
        :return: dict, which all the quote data
        """
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
        return self.clean_server_response(ast.literal_eval(match.group(1))['data'][0])


    def get_top_gainers(self):
        pass

    def get_top_losers(self):
        pass

    def nse_headers(self):
        """
        Builds right set of headers for requesting http://nseindia.com
        :return: http headers
        """
        return {'Accept' : '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Host':    'nseindia.com',
                'Referer': 'http://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=INFY&illiquid=0',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
                'X-Requested-With':    'XMLHttpRequest'
            }
    def nse_opener(self):
        """
        builds opener for urllib2
        :return: opener
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
        :return: dict, cleaned dictionary
        """
        for key, value in resp_dict.iteritems():
            if type(value) is str:
                if re.match('-', value):
                    resp_dict[key] = None
                elif re.search(r'^[0-9,.]+$', value):
                    # replace , to '', and type cast to int
                    resp_dict[key] = float(re.sub(',', '', value))
        return resp_dict

    def __str__(self):
        pass

if __name__ == '__main__':
    nse = Nse()
    import json
    print json.dumps(nse.get_quote('INFY'))