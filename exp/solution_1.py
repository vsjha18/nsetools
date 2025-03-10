import json

def parse_json(json_data):
    if isinstance(json_data, str):
        try:
            return int(json_data)
        except ValueError:
            try:
                return float(json_data)
            except ValueError:
                return json_data
    elif isinstance(json_data, dict):
        return {key: parse_json(value) for key, value in json_data.items()}
    elif isinstance(json_data, list):
        return [parse_json(item) for item in json_data]
    else:
        return json_data

# Example nested JSON with string-coated numbers
nested_json = '''
{
  "name": "John",
  "age": "30",
  "height": "175.5",
  "scores": ["90", "85", "95"],
  "details": {
    "weight": "75.5",
    "grades": ["80", "85", "90"]
  }
}
'''

# Parse the JSON and resolve string-coated numbers
parsed_data = parse_json(json.loads(nested_json))

# Access the resolved values
print(parsed_data["age"])  # Output: 30 (as an integer)
print(parsed_data["height"])  # Output: 175.5 (as a float)
print(parsed_data["scores"])  # Output: [90, 85, 95] (as a list of integers)
print(parsed_data["details"]["weight"])  # Output: 75.5 (as a float)
print(parsed_data["details"]["grades"])  # Output: [80, 85, 90] (as a list of integers)