import os

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