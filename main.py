import os
import scripts.file_loader as file_loader
import scripts.comparator as comparator
import scripts.output_writer as output_writer

# Define input paths
human_folder = "data/post_validation_human_annotations"
llm_folders = {
    "llama_3.1-8b": "data/llama_3.1-8b_output",
    "phi-4": "data/phi-4_output",
    "qwen_2.5-7b": "data/qwen_2.5-7b_output",
    "mistral-7b": "data/mistral-7b_output"
}
output_folder = "output"

# List of metrics we will compute and store in separate Excel files
metric_names = [
    "exact_match", "numeric_similarity", "jaccard_similarity",
    "normalized_exact_match", "similarity_90_match", "precision",
    "bleu_1", "recall", "rouge_1", "f1_score"
]

# Step 1: Check for missing files in each LLM folder
print("\n=== Checking for missing files in LLM folders ===")
for llm_name, llm_folder in llm_folders.items():
    file_loader.check_missing_files(human_folder, llm_folder, llm_name)

# Step 2: Iterate through each LLM, compare files, and store results
print("\n=== Running comparisons between Human Annotations and LLM Outputs ===")
for llm_name, llm_folder in llm_folders.items():
    print(f"\nProcessing: {llm_name}")

    # Get the list of annotation filenames from the human folder
    human_filenames = [f for f in os.listdir(human_folder) if f.endswith(".json")]

    comparison_results = []  # Store all comparison results for batch writing

    for filename in human_filenames:
        # Load human and LLM annotation files
        human_data = file_loader.load_json(human_folder, filename)
        llm_data = file_loader.load_json(llm_folder, filename)

        # Skip missing or invalid files
        if human_data is None or llm_data is None:
            print(f"Skipping {filename} due to missing data.")
            continue

        # Compare annotations
        result = comparator.compare_annotations(human_data, llm_data, filename)
        comparison_results.append(result)

    print(f"Completed comparisons for {llm_name}. Now writing results to Excel...")

    # Step 3: Extract and write results to Excel (one file per metric)
    for metric in metric_names:
        metric_results = []  # Store results for this metric

        for res in comparison_results:
            filename = res["filename"]  # Get filename

            # Initialize the metric entry
            metric_entry = {"filename": filename, "scores": {}}

            # Ensure correct metric extraction
            for var in [
                "age", "alternativeNames", "birthday", "descriptiveTexts", "directQuotes", "inIntro", "inTitle",
                "indirectQuotes", "isMain", "name", "occupations", "firstNameOnly", "fullName", "lastNameOnly",
                "total", "quotedInIntro", "quotedInTitle", "sex"
            ]:
                # If the metric applies to this variable, update it
                if var in res["scores"]:
                    value = res["scores"][var]  # Get the metric value

                    # If the value is a dictionary (multi-metric like precision, recall), extract the current metric
                    if isinstance(value, dict):
                        metric_entry["scores"][var] = round(value.get(metric, 0), 3)
                    else:
                        metric_entry["scores"][var] = round(value, 3)
                else:
                    metric_entry["scores"][var] = 0  # Ensure missing values are explicitly set to 0

            metric_results.append(metric_entry)  # Add structured result to list

        # Write results to Excel
        output_writer.write_results_to_excel(metric_results, metric, llm_name, output_folder)

print("\n=== All comparisons completed successfully! Results are stored in the output folder. ===")
