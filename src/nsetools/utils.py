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
import operator

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

def camel_to_title(camel_str):
    """Converts a camel case string to title case.
    This function takes a camel case string and converts it to title case by adding
    spaces before capital letters and capitalizing the first letter of each word.
    Args:
        camel_str (str): The camel case string to be converted.
    Returns:
        str: The converted string in title case format.
    Examples:
        >>> camel_to_title("camelCaseString")
        'Camel Case String'
        >>> camel_to_title("thisIsATest")
        'This Is A Test'
    """
    
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', camel_str).title()

def _resolve_path(data, path, case_insensitive=True):
    """Helper function to resolve dot notation paths in dictionaries."""
    if not path:
        return data
    
    parts = path.split('.')
    current = data
    
    for part in parts:
        if isinstance(current, dict):
            if case_insensitive:
                key_map = {k.lower(): k for k in current.keys()}
                part_lower = part.lower()
                if part_lower in key_map:
                    current = current[key_map[part_lower]]
                else:
                    return None
            else:
                current = current.get(part)
        else:
            return None
    return current

def _parse_query(query_str):
    """Parse query string into (path, operator, value) tuple."""
    operators = {
        '==': operator.eq,
        '!=': operator.ne,
        '>=': operator.ge,
        '<=': operator.le,
        '>': operator.gt,
        '<': operator.lt
    }
    
    for op_str, op_func in operators.items():
        if op_str in query_str:
            path, value = query_str.split(op_str)
            path = path.strip()
            value = value.strip()
            
            # Try to convert value to number if possible
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    # Keep as string if not numeric
                    pass
                    
            return path, op_func, value
            
    return None, None, None

def dict_to_table(data, title="Data Table", filter=None, ignore=None, sort=None, direction="desc", query=None):
    """Converts dictionary or list of dictionaries to a formatted table using Rich library.
    This function takes either a dictionary or a list of dictionaries and displays it as a
    formatted table in the console. It supports filtering specific keys, ignoring keys, and
    applies special formatting for negative numbers.
    Args:
        data (Union[dict, List[dict]]): The data to be displayed. Can be either a dictionary
            or a list of dictionaries.
        title (str, optional): The title to display above the table. Defaults to "Data Table".
        filter (List[str], optional): List of keys to include in the output. If provided,
            only these keys will be displayed. Keys are matched case-insensitively.
            Defaults to None.
        ignore (List[str], optional): List of keys to exclude from the output. Keys are
            matched case-insensitively. Defaults to None.
        sort (str, optional): Key to sort by. Case-insensitive. Will sort numerically 
            for numeric values and alphabetically for string values. Defaults to None.
        direction (str, optional): Sort direction - "asc" for ascending or "desc" for 
            descending. Defaults to "desc".
        query (str, optional): Filter rows using dot notation path and comparison.
            Supports operators: ==, !=, >, <, >=, <=
            Example: "market.price>100" or "status.active==True"
            Keys are matched case-insensitively. Defaults to None.
    """
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(title=title)

    if not data:
        console.print("[red]No data to display![/red]")
        return

    # Parse query if provided
    query_path = None
    query_op = None
    query_value = None
    if query:
        query_path, query_op, query_value = _parse_query(query)
        if not all([query_path, query_op, query_value]):
            console.print("[red]Invalid query format![/red]")
            return

    # Validate direction
    if direction not in ["asc", "desc"]:
        console.print("[red]Direction must be 'asc' or 'desc'![/red]")
        return

    # Normalize filter, ignore and sort keys
    if filter:
        if not isinstance(filter, list):
            console.print("[red]Filter should be a list of keys![/red]")
            return
        filter = [str(key).lower() for key in filter]
    
    if ignore:
        if not isinstance(ignore, list):
            console.print("[red]Ignore should be a list of keys![/red]")
            return
        ignore = [str(key).lower() for key in ignore]
    else:
        ignore = []

    if sort:
        sort = str(sort).lower()

    # Check if data is a list of dicts
    if isinstance(data, list) and all(isinstance(i, dict) for i in data):
        # Get all unique keys and create key mapping
        keys = set()
        for item in data:
            keys.update(item.keys())
        key_map = {k.lower(): k for k in keys}

        # Validate sort key if provided
        if sort and sort not in key_map:
            console.print(f"[red]Sort key '{sort}' not found in data![/red]")
            return

        # Create ordered keys list
        if filter:
            ordered_keys = [key_map[f] for f in filter if f in key_map and f not in ignore]
        else:
            ordered_keys = [key_map[k.lower()] for k in keys if k.lower() not in ignore]

        if not ordered_keys:
            console.print("[red]No matching keys found![/red]")
            return

        # Apply query filter before sorting
        if query:
            filtered_data = []
            for item in data:
                item_value = _resolve_path(item, query_path)
                if item_value is not None:
                    try:
                        if query_op(item_value, query_value):
                            filtered_data.append(item)
                    except TypeError:
                        # Handle type mismatch gracefully
                        continue
            data = filtered_data
            
            if not data:
                console.print("[red]No data matches the query![/red]")
                return

        # Sort data if sort key is provided
        if sort and sort in key_map:
            original_key = key_map[sort]
            # Try numeric sort first
            try:
                sorted_data = sorted(
                    data,
                    key=lambda x: float(x.get(original_key, 0)),
                    reverse=(direction == "desc")
                )
            except (ValueError, TypeError):
                # Fall back to string sort
                sorted_data = sorted(
                    data,
                    key=lambda x: str(x.get(original_key, "")),
                    reverse=(direction == "desc")
                )
        else:
            sorted_data = data

        # Add columns and display table
        for key in ordered_keys:
            table.add_column(camel_to_title(key), style="bright_white")

        for item in sorted_data:
            row = []
            for key in ordered_keys:
                value = item.get(key, "")
                if isinstance(value, (int, float)) and value < 0:
                    row.append(f"[red]{value}[/red]")
                else:
                    row.append(f"[bright_white]{value}[/bright_white]")
            table.add_row(*row)

    elif isinstance(data, dict):
        # Single dict can't be queried for rows
        if query:
            console.print("[red]Query is only supported for list of dictionaries![/red]")
            return

        # Filter and ignore the dictionary data
        filtered_data = {}
        key_map = {k.lower(): k for k in data.keys()}
        
        if filter:
            # Add keys in filter order if they exist and not in ignore
            for f in filter:
                if f in key_map and f not in ignore:
                    original_key = key_map[f]
                    value = data[original_key]
                    if not isinstance(value, (dict, list, tuple, set)):
                        filtered_data[original_key] = value
        else:
            # If no filter, exclude ignored and nested items
            filtered_data = {k: v for k, v in data.items() 
                           if not isinstance(v, (dict, list, tuple, set))
                           and k.lower() not in ignore}

        if not filtered_data:
            console.print("[red]No matching key-value pairs to display![/red]")
            return

        # Add columns
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="bright_white")

        # Add rows
        for key, value in filtered_data.items():
            if isinstance(value, (int, float)) and value < 0:
                value_str = f"[red]{value}[/red]"
            else:
                value_str = f"[bright_white]{value}[/bright_white]"
            table.add_row(camel_to_title(key), value_str)

    else:
        console.print("[red]Unsupported data format![/red]")
        return

    console.print(table)



