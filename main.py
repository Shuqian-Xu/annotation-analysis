import scripts

if __name__ == "__main__":
    human_folder = "data/post_validation_human_annotations"

    # Call the function using the full module path
    scripts.file_loader.check_missing_files(human_folder, "data/gemma_2-9b_output", "gemma_2-9b_output")
    scripts.file_loader.check_missing_files(human_folder, "data/llama_3.1-8b_output", "llama_3.1-8b_output")