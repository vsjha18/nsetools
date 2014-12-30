"""
    This is a test module for testing abstract base class
"""
import unittest
import logging
import json
from mock import Mock
from nselib.bases import AbstractBaseExchange
from nselib import Nse
import re

log = logging.getLogger('nse')
logging.basicConfig(level=logging.DEBUG)

class TestCoreAPIs(unittest.TestCase):
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
            'i': None,
            'j': u'10',
            'k': u'10.0',
            'l': u'1,000.10'
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
            'i': None,
            'j': 10,
            'k': 10.0,
            'l': 1000.10
        }
        ret_dict = self.nse.clean_server_response(test_dict)
        self.assertDictEqual(ret_dict, expected_dict)

    def test_get_stock_codes(self):
        sq = self.nse.get_stock_codes()
        self.assertIsNotNone(sq)
        self.assertIsInstance(sq, dict)

# TODO: use mock and create one test where response contains a blank line
# TODO: use mock and create one test where response doesnt contain a csv
# TODO: use mock and create one test where return is null
# TODO: test the cache feature

    def test_negative_get_quote(self):
        wrong_code = 'inf'
        self.assertIsNone(self.nse.get_quote(wrong_code))

    def test_get_quote(self):
        code = 'infy'
        self.assertIsInstance(self.nse.get_quote(code), dict)

    def test_is_valid_code(self):
        code = 'infy'
        self.assertTrue(self.nse.is_valid_code(code))

    def test_negative_is_valid_code(self):
        wrong_code = 'in'
        self.assertFalse(self.nse.is_valid_code(wrong_code))

    def test_get_top_gainers(self):
        res = self.nse.get_top_gainers()
        self.assertIsInstance(res, list)

    def test_get_top_losers(self):
        res = self.nse.get_top_losers()
        self.assertIsInstance(res, list)

    def test_render_response(self):
        d = {'fname':'vivek', 'lname':'jha'}
        resp_dict = self.nse.render_response('default', d)
        resp_json = self.nse.render_response('json', d)
        # in case of dict, response should be a python dict
        self.assertIsInstance(resp_dict, dict)
        # in case of json, response should be a json string
        self.assertIsInstance(resp_json, str)
        # and on reconstruction it should become same as original dict
        self.assertDictEqual(d, json.loads(resp_json))
        # and anything appart from json and dict should raise an error
        with self.assertRaises(Exception):
            self.nse.render_response('list', d)

    def test_advances_declines(self):
        resp = self.nse.get_advances_declines()
        # it should be a list of dictionaries
        self.assertIsInstance(resp, list)
        # get the json version
        resp_json = self.nse.get_advances_declines(ret_type='json')
        self.assertIsInstance(resp_json, str)
        # load the json response and it should have same number of
        # elements as in case of first response
        self.assertEqual(len(resp), len(json.loads(resp_json)))

    def test_is_valid_index(self):
        code = 'CNX NIFTY'
        self.assertTrue(self.nse.is_valid_index(code))
        # test with invalid string
        code = 'some junk stuff'
        self.assertFalse(self.nse.is_valid_index(code))
        # test with lower case
        code = 'cnx nifty'
        self.assertTrue(self.nse.is_valid_index(code))

    def test_get_index_quote(self):
        code = 'CNX NIFTY'
        self.assertIsInstance(self.nse.get_index_quote(code), dict)
        # with json response
        self.assertIsInstance(self.nse.get_index_quote(code, ret_type='json'),
                              str)
        # with wrong code
        code = 'wrong code'
        self.assertIsNone(self.nse.get_index_quote(code))

        # with lower case code
        code = 'cnx nifty'
        self.assertIsInstance(self.nse.get_index_quote(code), dict)

    def test_get_index_list(self):
        index_list = self.nse.get_index_list()
        index_list_json = self.nse.get_index_list(ret_type='json')
        self.assertIsInstance(index_list, list)
        # test json response type
        self.assertIsInstance(index_list_json, str)
        # reconstruct list from json and match
        self.assertListEqual(index_list, json.loads(index_list_json))

if __name__ == '__main__':
    unittest.main()
