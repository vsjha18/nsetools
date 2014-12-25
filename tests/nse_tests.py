"""
    This is a test module for testing abstract base class
"""
import unittest
import logging

from nselib.bases import AbstractBaseExchange
from nselib import Nse
import re

log = logging.getLogger('nse')
logging.basicConfig(level=logging.DEBUG)

class BaseClass(unittest.TestCase):
    def setUp(self):
        self.nse = Nse()

    def test_instantiate_abs_class(self):
        class Exchange(AbstractBaseExchange): pass
        with self.assertRaises(TypeError):
            exc = Exchange()

    def test_nse_headers(self):
        ret = self.nse.nse_headers()
        self.assertIsInstance(ret, dict)

    def test_nse_opener(self):
        ''' should not raise any exception '''
        opener = self.nse.nse_opener()

    def test_build_url_for_quote(self):
        test_code = 'infy'
        url = self.nse.build_url_for_quote(test_code)
        # 'test_code' should be present in the url
        self.assertIsNotNone(re.search(test_code, url))

    def test_negative_build_url_for_quote(self):
            negative_codes = [1, None]
            with self.assertRaises(Exception):
                for test_code in negative_codes:
                    url = self.nse.build_url_for_quote(test_code)

    def test_response_cleaner(self):
        test_dict = {
            'a': '10',
            'b': '10.0',
            'c': '1,000.10',
            'd': 'vsjha18',
            'e': 10,
            'f': 10.0,
            'g': 1000.10,
            'h': True,
            'i': None
        }

        expected_dict = {
            'a': 10,
            'b': 10.0,
            'c': 1000.10,
            'd': 'vsjha18',
            'e': 10,
            'f': 10.0,
            'g': 1000.10,
            'h': True,
            'i': None
        }
        ret_dict = self.nse.clean_server_response(test_dict)
        self.assertDictEqual(ret_dict, expected_dict)

if __name__ == '__main__':
    unittest.main()