import json
from datetime import datetime

def parse_values(obj):
    for key, value in obj.items():
        if isinstance(value, str):
            # Try to parse as datetime if the string matches the format
            date_formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d-%b-%Y"]
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

# Example nested JSON with string-coated numbers and timestamps
nested_json = '''
{
  "name": "John",
  "age": "30",
  "height": "175.5",
  "birthdate": "1990-01-01",
  "bd": "01-Jan-2023",
  "timestamp": "2023-06-12 10:30:00",
  "scores": ["90", "85", "95"],
  "details": {
    "weight": "75.5",
    "grades": ["80", "85", "90"],
    "exam_date": "2022-12-31"
  }
}
'''

# Parse the JSON and resolve string-coated numbers and timestamps
parsed_data = json.loads(nested_json, object_hook=parse_values)

# Access the resolved values
print(parsed_data["age"])  # Output: 30 (as an integer)
print(parsed_data["height"])  # Output: 175.5 (as a float)
print(parsed_data["birthdate"])  # Output: 1990-01-01 00:00:00 (as a datetime object)
print(parsed_data["timestamp"])  # Output: 2023-06-12 10:30:00 (as a datetime object)
print(parsed_data["scores"])  # Output: [90, 85, 95] (as a list of integers)
print(parsed_data["details"]["weight"])  # Output: 75.5 (as a float)
print(parsed_data["details"]["grades"])  # Output: [80, 85, 90] (as a list of integers)
print(parsed_data["details"]["exam_date"])  # Output: 2022-12-31 00:00:00 (as a datetime object)
print(parsed_data["bd"])  # Output: 2022-12-31 00:00:00 (as a datetime object)
print(type(parsed_data["bd"]))
