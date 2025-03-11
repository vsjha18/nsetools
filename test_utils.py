import sys 
import os 
import unittest
# Add at top with other imports

# os.path.join(os.environ.get('VIRTUAL_ENV'), "nsetools")
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from nsetools.utils import cast_intfloat_string_values_to_intfloat

class TestUtils(unittest.TestCase):
    def setUp(self):
        pass 
    
    def test_cast_intfloat_string_values_to_intfloat(self):
        sample = {'a': 'bangalore', 'b': '1', 'c': '100.21', 'd': True}
        resp = cast_intfloat_string_values_to_intfloat(sample)
        self.assertDictEqual(resp, {'a': 'bangalore', 'b': 1, 'c': 100.21, 'd': True})

if __name__ == '__main__':
    unittest.main()
