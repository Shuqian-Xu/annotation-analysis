import os
import scripts

if __name__ == "__main__":
    # human_folder = "data/post_validation_human_annotations"
    # gemma_folder = "data/gemma_2-9b_output"
    # llama_folder = "data/llama_3.1-8b_output"
    #
    # # Check if all files in the human annotations folder exist in the both LLM folders
    # scripts.file_loader.check_missing_files(human_folder, gemma_folder, "gemma_2-9b_output")
    # scripts.file_loader.check_missing_files(human_folder, llama_folder, "llama_3.1-8b_output")
    #
    # # Get all human annotation filenames
    # human_files = [f for f in os.listdir(human_folder) if os.path.isfile(os.path.join(human_folder, f))]
    #
    # for filename in human_files:
    #     # Load human annotation
    #     human_data = scripts.file_loader.load_json(human_folder, filename)
    #
    #     # Load corresponding LLM annotations (only if they exist and are valid)
    #     gemma_data = scripts.file_loader.load_json(gemma_folder, filename)
    #     llama_data = scripts.file_loader.load_json(llama_folder, filename)
    #
    #     # Skip files where LLM output is missing or invalid
    #     if gemma_data is None:
    #         print(f"Skipping {filename} - No valid Gemma annotation")
    #         continue
    #     if llama_data is None:
    #         print(f"Skipping {filename} - No valid Llama annotation")
    #         continue
    #
    #     # At this point, human_data, gemma_data, and llama_data are all valid
    #     print(f"Ready to compare {filename}")

    """
        Tests the comparator.py implementation using the given human and gemma 2-9b annotation files.
        Prints the results for verification.
        """
    human_folder = "data/post_validation_human_annotations"
    llm_folder = "data/gemma_2-9b_output"
    filename = "6cb137ab-8585-4952-86e5-aeca9472708a.json"

    # Load JSON data
    human_data = scripts.file_loader.load_json(human_folder, filename)
    llm_data = scripts.file_loader.load_json(llm_folder, filename)

    # Ensure files are loaded properly
    if human_data is None or llm_data is None:
        print(f"Error: Could not load {filename} for testing.")

    # Compare annotations
    result = scripts.comparator.compare_annotations(human_data, llm_data, filename)

    # Print formatted result
    print("\n=== Test: Comparison Result ===")
    print(f"Filename: {result['filename']}")

    for var, scores in result["scores"].items():
        if isinstance(scores, dict):  # Text-based metrics with multiple scores
            print(f"{var}:")
            for metric, value in scores.items():
                print(f"  {metric}: {value}")
        else:  # Single-score metrics
            print(f"{var}: {scores}")

    print("\n=== Test Completed ===")