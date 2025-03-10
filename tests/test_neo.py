import sys 
import os 
import unittest
# Add at top with other imports

# os.path.join(os.environ.get('VIRTUAL_ENV'), "nsetools")
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from nsetools import Nse
from nsetools.utils import cast_intfloat_string_values_to_intfloat


class TestIndexAPIs(unittest.TestCase):
    def setUp(self):
        self.nse = Nse()

    def test_get_index_list(self):
        index_list = self.nse.get_index_list()
        # Check type
        self.assertIsInstance(index_list, list)
        # Check for essential indices
        essential_indices = ['NIFTY 50', 'NIFTY BANK', 'NIFTY AUTO', 'NIFTY FMCG']
        for index in essential_indices:
            self.assertIn(index, index_list)
        # Check some basic properties
        self.assertTrue(len(index_list) > 20)  # Should have more than 20 indices
        self.assertTrue(all(isinstance(idx, str) for idx in index_list))  # All elements should be strings

    def test_get_index_quote(self):
        quote = self.nse.get_index_quote('nifty 50')
        
        # Check essential fields exist
        essential_fields = ['indexSymbol', 'last', 'variation', 'percentChange', 
                          'open', 'high', 'low', 'previousClose']
        for field in essential_fields:
            self.assertIn(field, quote)
        
        # Check types of numeric fields
        numeric_fields = ['last', 'variation', 'percentChange', 'open', 'high', 
                         'low', 'previousClose', 'pe', 'pb', 'dy']
        for field in numeric_fields:
            self.assertIsInstance(quote[field], (int, float))
        
        # Check specific values
        self.assertEqual(quote['indexSymbol'], 'NIFTY 50')
        self.assertEqual(quote['index'], 'NIFTY 50')
        
        # Verify advances + declines + unchanged equals 50 for NIFTY 50
        self.assertEqual(quote['advances'] + quote['declines'] + quote['unchanged'], 50)

    def test_get_all_index_quote(self):
        quotes = self.nse.get_all_index_quote()
        
        # Check basic structure
        self.assertIsInstance(quotes, list)
        self.assertTrue(len(quotes) > 20)  # Should have multiple indices
        
        # Check structure of a quote
        sample_quote = quotes[0]  # Take first quote
        essential_fields = ['indexSymbol', 'last', 'variation', 'percentChange', 
                          'open', 'high', 'low', 'previousClose']
        for field in essential_fields:
            self.assertIn(field, sample_quote)
        
        # Verify we have major indices in the list
        index_symbols = [quote['indexSymbol'] for quote in quotes]
        major_indices = ['NIFTY 50', 'NIFTY BANK', 'NIFTY AUTO']
        for idx in major_indices:
            self.assertIn(idx, index_symbols)
        
        # Check numeric types for first quote
        numeric_fields = ['last', 'variation', 'percentChange', 'open', 'high', 
                         'low', 'previousClose']
        for field in numeric_fields:
            self.assertIsInstance(sample_quote[field], (int, float))

    def test_get_advances_declines(self):
        # Test for NIFTY 50
        ad_data = self.nse.get_advances_declines('nifty 50')
        # Check structure
        self.assertIsInstance(ad_data, dict)
        self.assertIn('advances', ad_data)
        self.assertIn('declines', ad_data)
        
        # Check types
        self.assertIsInstance(ad_data['advances'], (int, float))
        self.assertIsInstance(ad_data['declines'], (int, float))
        
        # Verify total count matches index size
        self.assertLessEqual(ad_data['advances'] + ad_data['declines'], 50)
        
        # Test with different index
        bank_ad = self.nse.get_advances_declines('nifty bank')
        self.assertLessEqual(bank_ad['advances'] + bank_ad['declines'], 12)  # NIFTY Bank has 12 stocks

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

class TestMisc(unittest.TestCase):
    def setUp(self):
        pass 
    
    def test_cast_intfloat_string_values_to_intfloat(self):
        sample = {'a': 'bangalore', 'b': '1', 'c': '100.21', 'd': True}
        resp = cast_intfloat_string_values_to_intfloat(sample)
        self.assertDictEqual(resp, {'a': 'bangalore', 'b': 1, 'c': 100.21, 'd': True})

if __name__ == '__main__':
    unittest.main()
