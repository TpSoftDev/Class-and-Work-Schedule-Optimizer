import json


def count_json_objects(file_path):
    try:
        # Open the JSON file and read its contents
        with open(file_path, "r") as file:
            data = json.load(file)

        # Check if the data is a list
        if isinstance(data, list):
            # Return the number of JSON objects in the list
            return len(data)
        else:
            # If the data is not a list, return 1 if it's a dictionary (single JSON object)
            return 1 if isinstance(data, dict) else 0

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return 0
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


# Example usage
file_path = "data.json"
num_json_objects = count_json_objects(file_path)
print(f"The number of JSON objects in the file is: {num_json_objects}")
