import json
import pytest


def read_json(file_name):
    """Reads a JSON file and returns the data."""
    file_path = f"data/{file_name}"
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}")
        return []


def get_test_data(file_name, main_key, data_keys=None, key_val=False):
    """Obtain parameterized data tuples from a JSON file."""
    test_data = read_json(file_name)

    if not test_data or main_key not in test_data:
        pytest.skip(f"Skipping tests: Key '{main_key}' not found in JSON file '{file_name}'.")

    data_list = test_data[main_key]
    if not isinstance(data_list, list) or not data_list:
        pytest.skip(f"Skipping tests: No data found under key '{main_key}' in '{file_name}'.")

    if not key_val:
        return data_list

    extracted_data = []

    for item in data_list:
        try:
            extracted_data.append(tuple(item[key] for key in data_keys))
        except KeyError as e:
            pytest.skip(f"Missing expected key {e} in data item: {item}")

    return extracted_data
