import os
import json

def check_missing_files(human_folder: str, llm_folder: str, llm_name: str):
    """
    Checks if all files in the human annotations folder exist in the specified LLM folder.
    Prints filenames of missing files.

    :param human_folder: Path to the human annotation folder (benchmark)
    :param llm_folder: Path to the LLM annotation folder to compare
    :param llm_name: Name of the LLM model (for print messages)
    """
    # Get all filenames (excluding directories)
    human_files = set(f for f in os.listdir(human_folder) if os.path.isfile(os.path.join(human_folder, f)))
    llm_files = set(f for f in os.listdir(llm_folder) if os.path.isfile(os.path.join(llm_folder, f)))

    # Find missing files
    missing_files = human_files - llm_files  # Files present in human but not in LLM

    # Print each missing file on a new line
    if missing_files:
        for file in sorted(missing_files):
            print(f"{file} is missing in {llm_name} folder")
    else:
        print(f"No missing files in {llm_name} folder")

def load_json(folder: str, filename: str):
    """
    Loads a JSON file from the specified folder.

    :param folder: Path to the folder containing JSON files.
    :param filename: Name of the JSON file to load.
    :return: The JSON data as a dictionary (or list), or None if an error occurs.
    """
    if not filename.endswith(".json"):  # Ignore non-JSON files
        return None

    file_path = os.path.join(folder, filename)  # Construct full file path

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: {filename} not found in {folder}")
        return None

    # Try reading and parsing the JSON file
    try:
        with open(file_path, "r", encoding="utf-8") as f:  # Ensure UTF-8 decoding
            data = json.load(f)

        # Detect LLM error messages and exclude them
        if isinstance(data, dict) and "error" in data:
            print(f"Skipping {filename} in {folder} (LLM error file: {data['error']})")
            return None

        return data  # Return JSON content as a Python object (dict or list)

    except json.JSONDecodeError:
        print(f"Error: {filename} is not a valid JSON file in {folder}")
        return None
    except Exception as e:
        print(f"Unexpected error while reading {filename}: {e}")
        return None