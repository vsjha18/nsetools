import sys
import os
import unittest
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from nsetools import Nse


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

    def test_get_top_gainers_losers_internal(self):
        """Test internal _get_top_gainers_losers method"""
        # Test gainers for different indices
        gainers_nifty = self.nse._get_top_gainers_losers('gainers', 'NIFTY')
        gainers_banknifty = self.nse._get_top_gainers_losers('gainers', 'BANKNIFTY')
        gainers_all = self.nse._get_top_gainers_losers('gainers', 'ALL')

        # Verify structure and types
        for gainers in [gainers_nifty, gainers_banknifty, gainers_all]:
            self.assertIsInstance(gainers, list)
            if len(gainers) > 0:  # Only check if we have data
                self.assertIsInstance(gainers[0], dict)
                # Check essential fields in first entry
                sample = gainers[0]
                self.assertIn('symbol', sample)
                self.assertIn('ltp', sample)  # changed from lastPrice
                self.assertIn('net_price', sample)  # changed from change
                self.assertIn('perChange', sample)  # changed from pChange
                # Verify numeric fields
                self.assertIsInstance(sample['ltp'], (int, float))
                self.assertIsInstance(sample['net_price'], (int, float))
                self.assertIsInstance(sample['perChange'], (int, float))

        # Test invalid index
        with self.assertRaises(ValueError):
            self.nse._get_top_gainers_losers('gainers', 'INVALID')

    def test_get_top_gainers(self):
        """Test get_top_gainers public method"""
        # Test default parameter (NIFTY)
        gainers_default = self.nse.get_top_gainers()
        self.assertIsInstance(gainers_default, list)
        
        # Test with explicit index
        gainers_banknifty = self.nse.get_top_gainers('BANKNIFTY')
        self.assertIsInstance(gainers_banknifty, list)
        
        # Test with ALL
        gainers_all = self.nse.get_top_gainers('ALL')
        self.assertIsInstance(gainers_all, list)

        # Verify common structure if data exists
        if len(gainers_default) > 0:
            sample = gainers_default[0]
            self.assertIsInstance(sample, dict)
            self.assertIn('symbol', sample)
            self.assertIn('ltp', sample)  # changed from lastPrice
            self.assertTrue(sample['net_price'] > 0)  # changed from change

    def test_get_top_losers(self):
        """Test get_top_losers public method"""
        # Test default parameter
        losers_default = self.nse.get_top_losers()
        self.assertIsInstance(losers_default, list)
        
        # Test with explicit index
        losers_fno = self.nse.get_top_losers('FNO')
        self.assertIsInstance(losers_fno, list)
        
        # Test NIFTYNEXT50
        losers_next50 = self.nse.get_top_losers('NIFTYNEXT50')
        self.assertIsInstance(losers_next50, list)

        # Verify common structure if data exists
        if len(losers_default) > 0:
            sample = losers_default[0]
            self.assertIsInstance(sample, dict)
            self.assertIn('symbol', sample)
            self.assertIn('ltp', sample)  # changed from lastPrice
            self.assertTrue(sample['net_price'] < 0)  # changed from change

    def test_get_stocks_in_index(self):
        """Test getting list of stocks in an index"""
        # Test with default parameter (NIFTY 50)
        stocks = self.nse.get_stocks_in_index()
        self.assertIsInstance(stocks, list)
        self.assertEqual(len(stocks), 50)  # NIFTY 50 should have 50 stocks
        
        # Check for presence of major stocks
        major_stocks = ['RELIANCE', 'HDFCBANK', 'INFY', 'TCS', 'ICICIBANK']
        for stock in major_stocks:
            self.assertIn(stock, stocks)
            
        # Test with NIFTY BANK
        bank_stocks = self.nse.get_stocks_in_index('NIFTY BANK')
        self.assertIsInstance(bank_stocks, list)
        self.assertEqual(len(bank_stocks), 12)  # NIFTY BANK has 12 stocks
        
        # Check for bank stocks
        bank_names = ['HDFCBANK', 'ICICIBANK', 'AXISBANK', 'SBIN']
        for bank in bank_names:
            self.assertIn(bank, bank_stocks)
            
        # Test with lowercase input
        lower_case_stocks = self.nse.get_stocks_in_index('nifty 50')
        self.assertEqual(stocks, lower_case_stocks)  # Should be case insensitive
        
        # Test with invalid index
        with self.assertRaises(Exception):
            self.nse.get_stocks_in_index('INVALID_INDEX')

    def test_get_stock_quote_in_index(self):
        """Test getting stock quotes in an index"""
        # Test with default parameter (NIFTY 50, include_index=False)
        quotes = self.nse.get_stock_quote_in_index()
        self.assertIsInstance(quotes, list)
        self.assertEqual(len(quotes), 50)  # NIFTY 50 should have 50 quotes
        
        # Test with include_index=True
        quotes_with_index = self.nse.get_stock_quote_in_index(include_index=True)
        self.assertEqual(len(quotes_with_index), 51)  # 50 stocks + 1 index
        
        # Verify index record
        index_record = quotes_with_index[0]
        self.assertEqual(index_record['priority'], 1)  # Index has priority 1
        self.assertEqual(index_record['symbol'], 'NIFTY 50')
        
        # Verify stock records
        stock_records = quotes_with_index[1:]
        self.assertEqual(len(stock_records), 50)
        for quote in stock_records:
            self.assertEqual(quote['priority'], 0)  # Stocks have priority 0
        
        # Rest of basic validation
        sample_quote = quotes[0]
        essential_fields = [
            'priority', 'symbol', 'identifier', 'series', 
            'open', 'dayHigh', 'dayLow', 'lastPrice',
            'previousClose', 'change', 'pChange',
            'totalTradedVolume', 'totalTradedValue'
        ]
        for field in essential_fields:
            self.assertIn(field, sample_quote)
        
        # Verify data types
        self.assertEqual(sample_quote['priority'], 0)
        self.assertIsInstance(sample_quote['symbol'], str)
        self.assertIsInstance(sample_quote['open'], (int, float))
        self.assertIsInstance(sample_quote['totalTradedVolume'], (int, float))
        self.assertIsInstance(sample_quote['pChange'], (int, float))
        
        # Test NIFTY BANK with both include_index True and False
        bank_quotes = self.nse.get_stock_quote_in_index('NIFTY BANK')
        self.assertEqual(len(bank_quotes), 12)
        
        bank_quotes_with_index = self.nse.get_stock_quote_in_index('NIFTY BANK', include_index=True)
        self.assertEqual(len(bank_quotes_with_index), 13)  # 12 stocks + 1 index
        
        # Test case insensitivity
        lower_case_quotes = self.nse.get_stock_quote_in_index('nifty 50')
        self.assertEqual(len(quotes), len(lower_case_quotes))
        
        # Test invalid index
        with self.assertRaises(Exception):
            self.nse.get_stock_quote_in_index('INVALID_INDEX')

if __name__ == '__main__':
    unittest.main()
