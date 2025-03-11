import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from nsetools.utils import cast_intfloat_string_values_to_intfloat

class TestUtils(unittest.TestCase):
    def test_cast_dict_values(self):
        # Test dictionary with mixed types
        input_dict = {
            'int_str': '123',
            'float_str': '123.45',
            'text': 'abc',
            'existing_int': 456,
            'existing_float': 456.78
        }
        expected_dict = {
            'int_str': 123,
            'float_str': 123.45,
            'text': 'abc',
            'existing_int': 456,
            'existing_float': 456.78
        }
        result = cast_intfloat_string_values_to_intfloat(input_dict)
        self.assertEqual(result, expected_dict)

    def test_cast_list_values(self):
        # Test list with mixed types
        input_list = ['123', '456.78', 'abc', 789, 123.45]
        expected_list = [123, 456.78, 'abc', 789, 123.45]
        result = cast_intfloat_string_values_to_intfloat(input_list)
        self.assertEqual(result, expected_list)

    def test_non_string_values(self):
        # Test that non-string values remain unchanged
        input_data = {'a': 123, 'b': 456.78, 'c': None}
        result = cast_intfloat_string_values_to_intfloat(input_data)
        self.assertEqual(result, input_data)

if __name__ == '__main__':
    unittest.main()
