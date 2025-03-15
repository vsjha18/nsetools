import sys
import os
import unittest
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from nsetools import Nse


class TestDerivativesAPIs(unittest.TestCase):
    def setUp(self):
        self.nse = Nse()

    def test_get_future_quote_valid_code(self):
        fut_quote = self.nse.get_future_quote('RELIANCE')
        self.assertIsInstance(fut_quote, list)  # Changed from dict to list
        self.assertTrue(len(fut_quote) > 0)
        self.assertIsInstance(fut_quote[0], dict)  # Check first item is a dict

    def test_get_future_quote_invalid_code(self):
        # The API might return empty list for invalid codes instead of raising ValueError
        result = self.nse.get_future_quote('INVALID123')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_get_future_quote_with_expiry(self):
        # Test with expiry date parameter
        fut_quote = self.nse.get_future_quote('SBIN', expiry_date='27-Mar-2025')
        self.assertIsInstance(fut_quote, dict)  # Single quote should be dict when expiry specified
        self.assertEqual(fut_quote['expiryDate'], '27-Mar-2025')
        
        # Verify we have the basic structure
        required_fields = [
            'openPrice', 'highPrice', 'lowPrice', 'closePrice',
            'lastPrice', 'change', 'pChange'
        ]
        for field in required_fields:
            self.assertIn(field, fut_quote)

    def test_get_future_quote_response_structure(self):
        fut_quote = self.nse.get_future_quote('TCS')
        self.assertIsInstance(fut_quote, list)
        
        # Verify first quote structure
        quote = fut_quote[0]
        self.assertIsInstance(quote, dict)
        
        # Check required fields directly in quote
        required_fields = [
            'expiryDate',
            'openPrice',
            'highPrice',
            'lowPrice',
            'closePrice',
            'prevClose',
            'lastPrice',
            'change',
            'pChange',
            'numberOfContractsTraded',
            'totalTurnover'
        ]
        
        for field in required_fields:
            self.assertIn(field, quote, f"Missing field: {field}")


if __name__ == '__main__':
    unittest.main()
