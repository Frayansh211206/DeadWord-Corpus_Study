"""
classify.py
-----------
Classifies uses of "dead" in Multicultural London English (MLE) sentences
extracted from the London English Corpus.

Categories:
    1. LITERAL    - refers to actual death/absence of life
    2. INTENSIFIER - modifies adj/adv to mean "very/extremely"
    3. EVALUATIVE - predicative use meaning "boring/rubbish"

Usage:
    1. Add your sentences (one per line) to sentences.csv
    2. Set your ANTHROPIC_API_KEY as environment variable
    3. Run: python classify.py
    4. Output saved to results.csv

Author: [Your Name]
Course: SPC4004 - Exploring AI: Understanding and Applications
"""

import os
import csv
import json
import anthropic

# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------
INPUT_FILE  = "sentences.csv"
OUTPUT_FILE = "results.csv"
MODEL       = "claude-opus-4-7"

# ----------------------------------------------------------------------
# THE CLASSIFICATION PROMPT
# ----------------------------------------------------------------------
SYSTEM_PROMPT = """You are a linguistic researcher specialising in Multicultural \
London English (MLE). Your task is to classify how the word "dead" is used in \
spontaneous speech."""

USER_PROMPT_TEMPLATE = """Classify the use of "dead" in the sentence below into \
exactly ONE of three categories:

1. LITERAL    - refers to actual death, no longer alive, or non-functioning
                (e.g. "the cat is dead", "my phone's gone dead")
2. INTENSIFIER - modifies an adjective/adverb to mean "very" or "extremely"
                (e.g. "dead funny", "dead tired", "dead long")
3. EVALUATIVE - used predicatively to mean "boring", "rubbish" or "lifeless"
                (e.g. "the party's dead", "this place is dead")

Sentence: "{sentence}"

Respond with valid JSON only, in this exact format:
{{"category": "LITERAL" | "INTENSIFIER" | "EVALUATIVE", "justification": "one short sentence"}}"""


def classify_sentence(client, sentence):
    """Send one sentence to Claude and return the classification."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(sentence=sentence)}
        ]
    )
    raw_text = response.content[0].text.strip()
    # strip any markdown fences if model adds them
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()
    try:
        result = json.loads(raw_text)
        return result["category"].lower(), result["justification"]
    except (json.JSONDecodeError, KeyError):
        return "ERROR", raw_text


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("Set ANTHROPIC_API_KEY environment variable first.")

    client = anthropic.Anthropic(api_key=api_key)

    # Read input sentences
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Loaded {len(rows)} sentences. Classifying...\n")

    # Classify each one
    for i, row in enumerate(rows, 1):
        category, justification = classify_sentence(client, row["sentence"])
        row["llm_category"] = category
        row["llm_justification"] = justification
        # Mark agreement with manual category if present
        if "manual_category" in row and row["manual_category"]:
            row["agreement"] = "yes" if category == row["manual_category"].lower() else "no"
        print(f"[{i:>2}/{len(rows)}] {category.upper():<12} | {row['sentence']}")

    # Write results
    fieldnames = ["id", "sentence", "manual_category", "llm_category",
                  "llm_justification", "agreement"]
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    # Summary stats
    print("\n" + "=" * 50)
    print("CLASSIFICATION SUMMARY")
    print("=" * 50)
    categories = [r["llm_category"] for r in rows]
    for cat in ["intensifier", "literal", "evaluative", "error"]:
        count = categories.count(cat)
        pct = (count / len(rows)) * 100 if rows else 0
        print(f"  {cat.capitalize():<13}: {count:>3} ({pct:.1f}%)")

    if any(r.get("agreement") for r in rows):
        agreed = sum(1 for r in rows if r.get("agreement") == "yes")
        print(f"\n  LLM vs manual agreement: {agreed}/{len(rows)} "
              f"({(agreed/len(rows))*100:.1f}%)")

    print(f"\nResults written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
