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
    Test function for output_writer.py.
    Simulates writing metric scores and checks if statistics are computed correctly.
    """
    # Simulated test data (as if coming from comparator.py)
    test_results = [
        {
            "filename": "test_file_1.json",
            "scores": {
                "age": 0.8, "alternativeNames": 0.6, "birthday": 0.7, "descriptiveTexts": 0.5,
                "directQuotes": 0.9, "inIntro": 1.0, "inTitle": 0.4, "indirectQuotes": 0.3,
                "isMain": 0.2, "name": 1.0, "occupations": 0.75, "firstNameOnly": 0.5,
                "fullName": 0.6, "lastNameOnly": 0.7, "total": 0.8, "quotedInIntro": 0.9,
                "quotedInTitle": 0.4, "sex": 1.0
            }
        },
        {
            "filename": "test_file_2.json",
            "scores": {
                "age": 0.9, "alternativeNames": 0.5, "birthday": 0.6, "descriptiveTexts": 0.4,
                "directQuotes": 0.8, "inIntro": 0.9, "inTitle": 0.3, "indirectQuotes": 0.4,
                "isMain": 0.1, "name": 1.0, "occupations": 0.7, "firstNameOnly": 0.6,
                "fullName": 0.5, "lastNameOnly": 0.6, "total": 0.7, "quotedInIntro": 0.8,
                "quotedInTitle": 0.3, "sex": 1.0
            }
        }
    ]

    # Run the test (writing results to 'precision.xlsx' under the 'phi-4' sheet)
    scripts.output_writer.write_results_to_excel(test_results, metric_name="precision", llm_name="phi-4")

    print("Test for output_writer.py completed. Check 'output/precision.xlsx' -> 'phi-4' sheet.")
