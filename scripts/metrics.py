import re
import Levenshtein
from nltk.translate.bleu_score import sentence_bleu

def concatenate_texts(text_list):
    """
    Concatenates all "text" values into a single string, ensuring a consistent comparison format.

    :param text_list: List of dictionaries containing "text" keys.
    :return: A concatenated string.
    """
    if not isinstance(text_list, list):  # Ensure it's a list
        return ""

    extracted_texts = [entry["text"] for entry in text_list if isinstance(entry, dict) and "text" in entry]
    return " ".join(extracted_texts).strip()

def exact_match(human_value, llm_value, is_text_based=False):
    """
    Computes Exact Match for all variable types.

    :param human_value: The reference value from human annotation.
    :param llm_value: The predicted value from LLM annotation.
    :param is_text_based: Boolean indicating whether the variable is a text-based list (descriptiveTexts, directQuotes, indirectQuotes, occupations).
    :return: Exact match score (1 or 0).
    """
    # Case 1: Text-based variables (concatenate all "text" values and compare)
    if is_text_based:
        human_text = concatenate_texts(human_value)
        llm_text = concatenate_texts(llm_value)
        return 1 if human_text == llm_text else 0

    # Case 2: All other variable types (binary match)
    return 1 if human_value == llm_value else 0

def numeric_similarity(human_value, llm_value):
    """
    Computes the similarity between two numeric values.

    :param human_value: The reference numeric value from human annotation.
    :param llm_value: The predicted numeric value from LLM annotation.
    :return: A similarity score between 0 and 1.
    """
    # Ensure both values are integers
    if not isinstance(human_value, int) or not isinstance(llm_value, int):
        return 0  # If non-integer, treat as completely different

    # If both are 0, return similarity of 1
    if human_value == llm_value == 0:
        return 1

    # Ensure no division by zero
    max_value = max(human_value, llm_value)
    if max_value == 0:
        return 0  # If the maximum value is 0, similarity is undefined; return 0.

    # Compute numeric similarity and round to 3 decimal places
    similarity = 1 - abs(human_value - llm_value) / max_value
    return round(similarity, 3)


def jaccard_similarity(human_list, llm_list):
    """
    Computes the Jaccard Similarity between two lists of strings.

    :param human_list: List of strings from human annotation.
    :param llm_list: List of strings from LLM annotation.
    :return: Jaccard similarity score between 0 and 1.
    """
    # Extract "text" values if lists contain dictionaries
    if isinstance(human_list, list):
        human_list = [entry["text"] for entry in human_list if isinstance(entry, dict) and "text" in entry]
    if isinstance(llm_list, list):
        llm_list = [entry["text"] for entry in llm_list if isinstance(entry, dict) and "text" in entry]

    # Convert lists to sets for set operations
    human_set = set(human_list)
    llm_set = set(llm_list)

    # If both sets are empty, consider them a perfect match
    if not human_set and not llm_set:
        return 1.0

    # Compute Jaccard similarity and round to 3 decimal places
    intersection_size = len(human_set & llm_set)
    union_size = len(human_set | llm_set)

    similarity = intersection_size / union_size if union_size > 0 else 0.0
    return round(similarity, 3)

def normalize_text(text):
    """
    Normalizes text by converting to lowercase and removing punctuation and special symbols.

    :param text: The input string.
    :return: Normalized string.
    """
    return re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s]', '', text.lower()).strip()

def normalized_exact_match(human_texts, llm_texts):
    """
    Computes Normalized Exact Match for text-based variables.

    :param human_texts: List of "text" values from human annotation.
    :param llm_texts: List of "text" values from LLM annotation.
    :return: Exact match score (1 or 0).
    """
    # Concatenate all "text" values
    human_text = normalize_text(concatenate_texts(human_texts))
    llm_text = normalize_text(concatenate_texts(llm_texts))

    return 1 if human_text == llm_text else 0

def similarity_90_match(human_texts, llm_texts):
    """
    Computes 90% Similarity Match for text-based variables.

    :param human_texts: List of "text" values from human annotation.
    :param llm_texts: List of "text" values from LLM annotation.
    :return: Similarity score (1 or 0).
    """
    # Concatenate all "text" values
    human_text = concatenate_texts(human_texts)
    llm_text = concatenate_texts(llm_texts)

    # Compute similarity using Levenshtein distance
    len_human = len(human_text)
    len_llm = len(llm_text)

    if max(len_human, len_llm) == 0:
        return 1  # If both are empty, return perfect match

    similarity = 1 - (Levenshtein.distance(human_text, llm_text) / max(len_human, len_llm))

    return 1 if similarity >= 0.9 else 0

def precision(human_texts, llm_texts):
    """
    Computes Precision for text-based variables.

    :param human_texts: List of "text" dictionaries from human annotation.
    :param llm_texts: List of "text" dictionaries from LLM annotation.
    :return: Precision score between 0 and 1.
    """
    # Ensure both inputs are lists; if None, set them to empty lists
    human_texts = human_texts if isinstance(human_texts, list) else []
    llm_texts = llm_texts if isinstance(llm_texts, list) else []

    # Extract "text" values from dictionaries
    if isinstance(human_texts, list):
        human_texts = [entry["text"] for entry in human_texts if isinstance(entry, dict) and "text" in entry]
    if isinstance(llm_texts, list):
        llm_texts = [entry["text"] for entry in llm_texts if isinstance(entry, dict) and "text" in entry]

    # Convert to sets to compare unique values
    human_set = set(human_texts)
    llm_set = set(llm_texts)

    # If LLM provides no annotations, return 1.0 (no false positives)
    if not llm_set:
        return 1.0

    # Compute precision and round to 3 decimal places
    true_positives = len(human_set & llm_set)
    false_positives = len(llm_set - human_set)

    precision_score = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0

    return round(precision_score, 3)

def bleu_1(human_texts, llm_texts):
    """
    Computes BLEU-1 score for text-based variables.

    :param human_texts: List of "text" values from human annotation.
    :param llm_texts: List of "text" values from LLM annotation.
    :return: BLEU-1 score between 0 and 1.
    """
    # Concatenate all "text" values
    human_text = concatenate_texts(human_texts)
    llm_text = concatenate_texts(llm_texts)

    # Tokenize words using simple whitespace split
    human_tokens = human_text.split()
    llm_tokens = llm_text.split()

    # Compute BLEU-1 score and round to 3 decimal places (using unigrams only)
    if len(llm_tokens) == 0:  # If LLM provided no output, return 0
        return 0.0

    bleu_score = sentence_bleu([human_tokens], llm_tokens, weights=(1.0, 0, 0, 0))

    return round(bleu_score, 3)

def recall(human_texts, llm_texts):
    """
    Computes Recall for text-based variables.

    :param human_texts: List of "text" dictionaries from human annotation.
    :param llm_texts: List of "text" dictionaries from LLM annotation.
    :return: Recall score between 0 and 1.
    """
    # Ensure both inputs are lists; if None, set them to empty lists
    human_texts = human_texts if isinstance(human_texts, list) else []
    llm_texts = llm_texts if isinstance(llm_texts, list) else []

    # Extract "text" values from dictionaries
    if isinstance(human_texts, list):
        human_texts = [entry["text"] for entry in human_texts if isinstance(entry, dict) and "text" in entry]
    if isinstance(llm_texts, list):
        llm_texts = [entry["text"] for entry in llm_texts if isinstance(entry, dict) and "text" in entry]

    # Convert to sets to compare unique values
    human_set = set(human_texts)
    llm_set = set(llm_texts)

    # If human annotation is empty, return 1.0 (no missing values)
    if not human_set:
        return 1.0

    # Compute recall and round to 3 decimal places
    true_positives = len(human_set & llm_set)
    false_negatives = len(human_set - llm_set)

    recall_score = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0

    return round(recall_score, 3)

def rouge_1(human_texts, llm_texts):
    """
    Computes ROUGE-1 score for text-based variables.

    :param human_texts: List of "text" values from human annotation.
    :param llm_texts: List of "text" values from LLM annotation.
    :return: ROUGE-1 score between 0 and 1.
    """
    # Concatenate all "text" values
    human_text = concatenate_texts(human_texts)
    llm_text = concatenate_texts(llm_texts)

    # Tokenize words using simple whitespace split (unigrams)
    human_tokens = set(human_text.split())
    llm_tokens = set(llm_text.split())

    # Compute ROUGE-1 score and round to 3 decimal places
    if len(human_tokens) == 0:  # If human annotation is empty, return 1
        return 1.0

    matching_unigrams = len(human_tokens & llm_tokens)  # Overlapping unigrams
    rouge_score = matching_unigrams / len(human_tokens)

    return round(rouge_score, 3)

def f1_score(human_texts, llm_texts):
    """
    Computes F1 Score for text-based variables.

    :param human_texts: List of "text" values from human annotation.
    :param llm_texts: List of "text" values from LLM annotation.
    :return: F1 Score between 0 and 1.
    """
    # Compute Precision and Recall using existing functions
    precision_score = precision(human_texts, llm_texts)
    recall_score = recall(human_texts, llm_texts)

    # Compute F1 Score and round to 3 decimal places.
    if precision_score + recall_score == 0:
        return 0.0  # Avoid division by zero

    f1 = 2 * (precision_score * recall_score) / (precision_score + recall_score)

    return round(f1, 3)
