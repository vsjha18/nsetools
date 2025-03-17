"""
    The MIT License (MIT)

    Copyright (c) 2014 Vivek Jha

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""
import six
import re


def byte_adaptor(fbuffer):
    """ provides py3 compatibility by converting byte based
    file stream to string based file stream

    Arguments:
        fbuffer: file like objects containing bytes

    Returns:
        string buffer
    """
    if six.PY3:
        strings = fbuffer.read().decode('latin-1')
        fbuffer = six.StringIO(strings)
        return fbuffer
    else:
        return fbuffer


def js_adaptor(buffer):
    """ convert javascript objects like true, none, NaN etc. to
    quoted word.

    Arguments:
        buffer: string to be converted

    Returns:
        string after conversion
    """
    buffer = re.sub('true', 'True', buffer)
    buffer = re.sub('false', 'False', buffer)
    buffer = re.sub('none', 'None', buffer)
    buffer = re.sub('NaN', '"NaN"', buffer)
    return buffer

def cast_intfloat_string_values_to_intfloat(data, round_digits=2):
    """Recursively converts string representations of numbers to integers or floats in nested data structures.
    This function traverses through dictionaries and lists, converting string values that represent
    numbers into their corresponding numeric types (int or float). For float values, it rounds to
    the specified number of decimal places.
    Args:
        data (Union[dict, list]): The input data structure containing values to be converted.
            Can be either a dictionary or a list, potentially nested.
        round_digits (int, optional): Number of decimal places to round float values to.
            Defaults to 2.
    Returns:
        Union[dict, list]: A new data structure of the same type as input, with string
            representations of numbers converted to their numeric types.
    Example:
        >>> data = {'a': '1', 'b': '2.5', 'c': 'text', 'd': {'e': '3.14'}}
        >>> cast_intfloat_string_values_to_intfloat(data)
        {'a': 1, 'b': 2.5, 'c': 'text', 'd': {'e': 3.14}}
    """

    if isinstance(data, dict):
        data = data.copy()
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    data[key] = int(value)
                except ValueError:
                    try:
                        data[key] = round(float(value), round_digits)
                    except ValueError:
                        pass
            elif isinstance(value, (dict, list)):
                data[key] = cast_intfloat_string_values_to_intfloat(value, round_digits)
            elif isinstance(value, float):
                data[key] = round(value, round_digits)
    elif isinstance(data, list):
        data = data[:]
        for i, value in enumerate(data):
            if isinstance(value, str):
                try:
                    data[i] = int(value)
                except ValueError:
                    try:
                        data[i] = round(float(value), round_digits)
                    except ValueError:
                        pass
            elif isinstance(value, (dict, list)):
                data[i] = cast_intfloat_string_values_to_intfloat(value, round_digits)
            elif isinstance(value, float):
                data[i] = round(value, round_digits)
    return data


