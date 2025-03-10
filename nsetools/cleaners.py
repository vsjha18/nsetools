"""
Module for various data structure cleaning tasks
"""
from datetime import datetime
dirty_data = """
{
    "fname": "Jon",
    "lname": "Doe",
    "age": 20,
    "str_age": "20",
    "pi": 3.1415927,
    "str_pi": "3.1415927",
    "dob": "01-Jan-2023",
    "mobile": [
        {
            "id": "Home",
            "number": "123456789"
        }, 
        {
            "id": "office", 
            "number": "987645321"
        }
    ] 
}
"""

def parse_values(obj):
    for key, value in obj.items():
        if isinstance(value, str):
            # Try to parse as datetime if the string matches the format
            date_formats = ["%d-%b-%Y", "%d-%m-%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
            for date_format in date_formats:
                try:
                    obj[key] = datetime.strptime(value, date_format)
                    break
                except ValueError:
                    pass
            else:
                # If the string couldn't be parsed as datetime, try numeric conversion
                try:
                    obj[key] = int(value)
                except ValueError:
                    try:
                        obj[key] = float(value)
                    except ValueError:
                        pass
        elif isinstance(value, dict):
            obj[key] = parse_values(value)
        elif isinstance(value, list):
            obj[key] = [parse_values(item) if isinstance(item, dict) else item for item in value]
    return obj
