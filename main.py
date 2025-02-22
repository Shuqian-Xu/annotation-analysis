import os
import scripts

if __name__ == "__main__":
    human_folder = "data/post_validation_human_annotations"
    gemma_folder = "data/gemma_2-9b_output"
    llama_folder = "data/llama_3.1-8b_output"

    # Check if all files in the human annotations folder exist in the both LLM folders
    scripts.file_loader.check_missing_files(human_folder, gemma_folder, "gemma_2-9b_output")
    scripts.file_loader.check_missing_files(human_folder, llama_folder, "llama_3.1-8b_output")

    # Get all human annotation filenames
    human_files = [f for f in os.listdir(human_folder) if os.path.isfile(os.path.join(human_folder, f))]

    for filename in human_files:
        # Load human annotation
        human_data = scripts.file_loader.load_json(human_folder, filename)

        # Load corresponding LLM annotations (only if they exist and are valid)
        gemma_data = scripts.file_loader.load_json(gemma_folder, filename)
        llama_data = scripts.file_loader.load_json(llama_folder, filename)

        # Skip files where LLM output is missing or invalid
        if gemma_data is None:
            print(f"Skipping {filename} - No valid Gemma annotation")
            continue
        if llama_data is None:
            print(f"Skipping {filename} - No valid Llama annotation")
            continue

        # At this point, human_data, gemma_data, and llama_data are all valid
        print(f"Ready to compare {filename}")