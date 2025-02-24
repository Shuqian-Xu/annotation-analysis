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

    print("Testing Metrics for Descriptive Texts...")

    # Human annotation descriptiveTexts
    human_texts = [
        "Antje Heinemann-Sanders lebt in einem kleinen, norddeutschen Idyll.",
        "Die zwei Pferde und das Pony, »so ein freches«, hat Heinemann-Sanders längst anderswo untergebracht.",
        "Noch kann sie in ihrem Haus bleiben.",
        "Mit einem großen Anhänger fahren sie vors Haus, Heinemann-Sanders, die Tochter, die Schwester und Marco Kirchner, der Nachbar.",
        "»Der Hänger trägt zwar ein ganzes Pferd, aber keine 30 Säcke«, sagt Heinemann-Sanders später.",
        "Sie ärgert sich über die Organisation.",
        "Im alten Dorf in Bümmerstede hätten sie alle eine Elementarschadenversicherung, sagt Antje Heinemann-Sanders.",
        "Und sie wüsste nicht, was die Versicherung zahle.",
        "Sie werde sichern, was möglich ist; Holzpflöcke und Pflastersteine unter die Möbel stellen."
    ]

    # Gemma 2-9b annotation descriptiveTexts
    gemma_texts = [
        "Antje Heinemann-Sanders lebt in einem kleinen, norddeutschen Idyll.",
        "Die zwei Pferde und das Pony, »so ein freches«, hat Heinemann-Sanders längst anderswo untergebracht.",
        "Noch kann sie in ihrem Haus bleiben.",
        "Mit einem großen Anhänger fahren sie vors Haus, Heinemann-Sanders, die Tochter, die Schwester und Marco Kirchner, der Nachbar.",
        "Sie wollten die rationierten 15 Sandsäcke abholen, die jedem Haushalt zustehen.",
        "Bekommen haben sie nur 30 Säcke, mehr hätten die Helfer nicht aufladen wollen, wegen des Gewichts.",
        "»Der Hänger trägt zwar ein ganzes Pferd, aber keine 30 Säcke«, sagt Heinemann-Sanders später.",
        "Sie ärgert sich über die Organisation.",
        "So sollen sie das Wasser aufhalten, falls es weiter über die Ufer tritt oder falls Deiche brechen.",
        "Den größten Teil der Schäden könne man noch gar nicht beziffern, da sie derzeit noch unter Wasser lägen.",
        "Im alten Dorf in Bümmerstede hätten sie alle eine Elementarschadenversicherung, sagt Antje Heinemann-Sanders.",
        "Und sie wüsste nicht, was die Versicherung zahle.",
        "»Hundert Quadratmeter Parkettboden – wissen Sie, wie viel das kostet?«",
        "Sie werde sichern, was möglich ist; Holzpflöcke und Pflastersteine unter die Möbel stellen."
    ]

    # Running all relevant metrics
    print("Exact Match:", scripts.metrics.exact_match(human_texts, gemma_texts))
    print("Normalized Exact Match:", scripts.metrics.normalized_exact_match(human_texts, gemma_texts))
    print("90% Similarity Match:", scripts.metrics.similarity_90_match(human_texts, gemma_texts))
    print("Precision:", scripts.metrics.precision(human_texts, gemma_texts))
    print("BLEU-1:", scripts.metrics.bleu_1(human_texts, gemma_texts))
    print("Recall:", scripts.metrics.recall(human_texts, gemma_texts))
    print("ROUGE-1:", scripts.metrics.rouge_1(human_texts, gemma_texts))
    print("F1 Score:", scripts.metrics.f1_score(human_texts, gemma_texts))

    print("Descriptive Texts Test Completed!")
