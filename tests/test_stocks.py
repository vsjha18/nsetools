import sys
import os
import unittest
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from nsetools import Nse
from nsetools.utils import cast_intfloat_string_values_to_intfloat


class TestStockAPIs(unittest.TestCase):
    def setUp(self):
        self.nse = Nse()

    def test_get_quote(self):
        quote = self.nse.get_quote('infy')
        # Check if basic keys exist
        self.assertIn('lastPrice', quote)
        self.assertIn('previousClose', quote)
        self.assertIn('change', quote)
        
        # Check numeric type of important values
        self.assertIsInstance(quote['lastPrice'], (int, float))
        self.assertIsInstance(quote['previousClose'], (int, float))
        self.assertIsInstance(quote['change'], (int, float))
        
        # Check nested dictionary
        self.assertIn('weekHighLow', quote)
        self.assertIsInstance(quote['weekHighLow'], dict)
        self.assertIsInstance(quote['weekHighLow']['min'], (int, float))
        self.assertIsInstance(quote['weekHighLow']['max'], (int, float))

    def test_get_stock_codes(self):
        stock_codes = self.nse.get_stock_codes()
        self.assertIsInstance(stock_codes, list)
        self.assertTrue(len(stock_codes) > 0)
        # Test for presence of major stocks
        self.assertTrue('RELIANCE' in stock_codes)
        self.assertTrue('TCS' in stock_codes)
        self.assertTrue('INFY' in stock_codes)

    def test_is_valid_code(self):
        # Test valid codes with different cases
        self.assertTrue(self.nse.is_valid_code('INFY'))
        self.assertTrue(self.nse.is_valid_code('infy'))  # Should work with lowercase too
        self.assertTrue(self.nse.is_valid_code('Tcs'))   # Should work with mixed case
        
        # Test invalid codes
        self.assertFalse(self.nse.is_valid_code('INVALID123'))
        self.assertFalse(self.nse.is_valid_code(''))     # Empty string case
        
        # Test None case
        with self.assertRaises(AttributeError):          # None case should raise AttributeError
            self.nse.is_valid_code(None)

    def test_get_52_week_high(self):
        """Test to get 52 week high data from NSE"""
        data = self.nse.get_52_week_high()
        self.assertIsInstance(data, list)
        if len(data) > 0:
            record = data[0]
            self.assertIsInstance(record, dict)
            required_fields = ['symbol', 'series', 'comapnyName', 'new52WHL', 
                             'prev52WHL', 'prevHLDate', 'ltp', 'prevClose', 
                             'change', 'pChange']
            for field in required_fields:
                self.assertIn(field, record)
            self.assertIsInstance(record['symbol'], str)
            self.assertIsInstance(record['new52WHL'], (int, float))
            self.assertIsInstance(record['pChange'], (int, float))

    def test_get_52_week_low(self):
        """Test to get 52 week low data from NSE"""
        data = self.nse.get_52_week_low()
        self.assertIsInstance(data, list)
        if len(data) > 0:
            record = data[0]
            self.assertIsInstance(record, dict)
            required_fields = ['symbol', 'series', 'comapnyName', 'new52WHL', 
                             'prev52WHL', 'prevHLDate', 'ltp', 'prevClose', 
                             'change', 'pChange']
            for field in required_fields:
                self.assertIn(field, record)
            self.assertIsInstance(record['symbol'], str)
            self.assertIsInstance(record['new52WHL'], (int, float))
            self.assertIsInstance(record['pChange'], (int, float))


class TestMisc(unittest.TestCase):
    def setUp(self):
        pass

    def test_cast_intfloat_string_values_to_intfloat(self):
        sample = {'a': 'bangalore', 'b': '1', 'c': '100.21', 'd': True}
        resp = cast_intfloat_string_values_to_intfloat(sample)
        self.assertDictEqual(resp, {'a': 'bangalore', 'b': 1, 'c': 100.21, 'd': True})


if __name__ == '__main__':
    unittest.main()
