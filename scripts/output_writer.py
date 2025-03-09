import pandas as pd
import os

def write_results_to_excel(results, metric_name, llm_name, output_folder="output"):
    """
    Writes comparison results to the corresponding Excel file and sheet.

    :param results: List of dictionaries containing filename and metric scores.
    :param metric_name: The name of the metric (determines which Excel file to update).
    :param llm_name: The name of the LLM model (determines which sheet to update).
    :param output_folder: Folder where the output Excel files are stored.
    """
    # Define the path to the correct Excel file
    excel_path = os.path.join(output_folder, f"{metric_name}.xlsx")

    # Load the existing Excel file
    if os.path.exists(excel_path):
        df_existing = pd.read_excel(excel_path, sheet_name=llm_name)
    else:
        raise FileNotFoundError(f"Excel file {metric_name}.xlsx not found in {output_folder}.")

    # Convert results into a DataFrame
    rows = []
    for result in results:
        row_data = [result["filename"]]  # Column A: filename
        row_data.extend([result["scores"].get(var, 0) for var in [
            "age", "alternativeNames", "birthday", "descriptiveTexts", "directQuotes", "inIntro", "inTitle",
            "indirectQuotes", "isMain", "name", "occupations", "firstNameOnly", "fullName", "lastNameOnly", "total",
            "quotedInIntro", "quotedInTitle", "sex"
        ]])
        rows.append(row_data)

    df_new = pd.DataFrame(rows, columns=df_existing.columns.tolist())

    # Append new data to the existing sheet
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)

    # Compute Mean, Median, and Standard Deviation
    summary_stats = df_combined.iloc[:, 1:].apply(pd.to_numeric, errors="coerce").agg(["mean", "median", "std"]).round(3)

    # Convert summary stats into a DataFrame while ensuring "File" is in Column A
    summary_labels = ["Mean", "Median", "Standard Deviation"]
    df_summary = pd.DataFrame(summary_stats)
    df_summary.insert(0, "File", summary_labels)  # Ensure correct placement in Column A

    # Concatenate final DataFrame
    df_final = pd.concat([df_combined, df_summary], ignore_index=True)

    # Save back to the Excel file
    with pd.ExcelWriter(excel_path, mode="a", if_sheet_exists="replace") as writer:
        df_final.to_excel(writer, sheet_name=llm_name, index=False)

    print(f"Results written to {metric_name}.xlsx (Sheet: {llm_name})")
