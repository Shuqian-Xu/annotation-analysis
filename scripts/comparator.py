import scripts.metrics as metrics

def compare_annotations(human_data, llm_data, filename):
    """
    Compares human and LLM annotations for a single file.

    :param human_data: The JSON data from human annotation.
    :param llm_data: The JSON data from LLM annotation.
    :param filename: The name of the annotation file.
    :return: Dictionary containing metric scores for all 18 variables.
    """
    human_persons = {p["name"]: p for p in human_data.get("persons", [])}
    llm_persons = {p["name"]: p for p in llm_data.get("persons", [])}

    matched_names = set(human_persons.keys()) & set(llm_persons.keys())
    extra_in_human = set(human_persons.keys()) - matched_names
    extra_in_llm = set(llm_persons.keys()) - matched_names

    all_variable_scores = {var: [] for var in [
        "age", "alternativeNames", "birthday", "descriptiveTexts", "directQuotes", "inIntro", "inTitle",
        "indirectQuotes", "isMain", "name", "occupations", "firstNameOnly", "fullName", "lastNameOnly", "total",
        "quotedInIntro", "quotedInTitle", "sex"
    ]}

    # Compare matched persons
    for name in matched_names:
        human_p = human_persons[name]
        llm_p = llm_persons[name]

        for var in all_variable_scores.keys():
            # Handle occurrence-based variables (firstNameOnly, fullName, lastNameOnly, total)
            if var in ["firstNameOnly", "fullName", "lastNameOnly", "total"]:
                human_occurrences = human_p.get("occurrences", human_p.get("occurences", {}))
                llm_occurrences = llm_p.get("occurrences", llm_p.get("occurences", {}))

                human_value = human_occurrences.get(var, 0)
                llm_value = llm_occurrences.get(var, 0)
            else:
                # Standard variables (age, alternativeNames, etc.)
                human_value = human_p.get(var, None)
                llm_value = llm_p.get(var, None)

            # Metric scores are 0 if LLM variable is missing
            if llm_value is None:
                if var in ["descriptiveTexts", "directQuotes", "indirectQuotes", "occupations"]:
                    score = {
                        "exact_match": 0,
                        "normalized_exact_match": 0,
                        "similarity_90_match": 0,
                        "precision": 0,
                        "bleu_1": 0,
                        "recall": 0,
                        "rouge_1": 0,
                        "f1_score": 0
                    }
                else:
                    score = 0  # For all other variables
                all_variable_scores[var].append(score)
                continue  # Skip metric calculation for missing values

            # Apply appropriate metric
            metric_scores = {
                "exact_match": metrics.exact_match(human_value, llm_value),
            }

            if var in ["age", "firstNameOnly", "fullName", "lastNameOnly", "total"]:
                metric_scores["numeric_similarity"] = metrics.numeric_similarity(human_value, llm_value)
            elif var == "alternativeNames":
                metric_scores["jaccard_similarity"] = metrics.jaccard_similarity(human_value, llm_value)
            elif var in ["descriptiveTexts", "directQuotes", "indirectQuotes", "occupations"]:
                metric_scores.update({
                    "normalized_exact_match": metrics.normalized_exact_match(human_value, llm_value),
                    "similarity_90_match": metrics.similarity_90_match(human_value, llm_value),
                    "precision": metrics.precision(human_value, llm_value),
                    "bleu_1": metrics.bleu_1(human_value, llm_value),
                    "recall": metrics.recall(human_value, llm_value),
                    "rouge_1": metrics.rouge_1(human_value, llm_value),
                    "f1_score": metrics.f1_score(human_value, llm_value)
                })

            all_variable_scores[var].append(metric_scores)

    # Handle persons extra or missing in LLM annotation files
    for name in extra_in_human | extra_in_llm:
        for var in all_variable_scores.keys():
            metric_scores = {
                "exact_match": 0,
            }

            if var in ["age", "firstNameOnly", "fullName", "lastNameOnly", "total"]:
                metric_scores["numeric_similarity"] = 0
            elif var == "alternativeNames":
                metric_scores["jaccard_similarity"] = 0
            elif var in ["descriptiveTexts", "directQuotes", "indirectQuotes", "occupations"]:
                metric_scores.update({
                    "normalized_exact_match": 0,
                    "similarity_90_match": 0,
                    "precision": 0,
                    "bleu_1": 0,
                    "recall": 0,
                    "rouge_1": 0,
                    "f1_score": 0
                })

            all_variable_scores[var].append(metric_scores)

    # Compute final scores per variable
    final_scores = {}

    for var, scores in all_variable_scores.items():
        if not scores:  # If scores is empty, assign 0 to avoid IndexError
            final_scores[var] = 0
            continue

        if all(isinstance(s, dict) for s in scores):  # Ensure all values are dictionaries (multi-metric)
            final_scores[var] = {
                metric: sum(s[metric] for s in scores) / len(scores) for metric in scores[0]
            }
        elif all(isinstance(s, (int, float)) for s in scores):  # Ensure all values are numbers (single-metric)
            final_scores[var] = sum(scores) / len(scores) if scores else 0
        else:
            final_scores[var] = 0  # Fallback for any unexpected cases

    return {"filename": filename, "scores": final_scores}
