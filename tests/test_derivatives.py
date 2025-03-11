import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from nsetools import Nse


class TestDerivativesAPIs(unittest.TestCase):
    def setUp(self):
        self.nse = Nse()

    # TODO: Add tests for derivatives related functionality
    # Example: Future contracts, options chain, etc.


if __name__ == '__main__':
    unittest.main()
