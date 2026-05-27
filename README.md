# DeadWord-Corpus_Study
A corpus-based linguistic analysis of how “dead” is used in Multicultural London English, using 215 examples from the London English Corpus and AI-assisted classification to compare literal, intensifier, and evaluative meanings.
# "Dead" in Multicultural London English — Dataset & Code

This repository contains the dataset, classification code, and results for
**SPC4004 Assessment 3: Analyzing Natural Language Data**.

## Research Question

How is the word **"dead"** used in Multicultural London English (MLE), and what
distinct functional categories of use can be identified across speaker
demographics?

## Headline finding

Of 215 instances of *dead* in the London English Corpus:

| Category    | n   | %     |
|-------------|-----|-------|
| Literal     | 183 | 85.1% |
| Evaluative  | 15  | 7.0%  |
| Intensifier | 12  | 5.6%  |
| Unclear     | 5   | 2.3%  |

Black/Mixed-heritage speakers used the evaluative ("place is dead") sense at
**25%**, almost 4x the rate of White British speakers (6.7%).

## Files

| File | Description |
|------|-------------|
| `classified_sentences.csv` | All 215 sentences with manual + LLM classification |
| `manual_classifications.csv` | Author's manual category labels |
| `classify.py` | Python script that classifies sentences using Claude API |
| `chart1_overall.png` | Bar chart of overall distribution |
| `chart2_demographic.png` | Stacked bar by speaker demographic |
| `report.pdf` | The 500-word report submitted for the assessment |

## Data source

Sentences were extracted from the **London English Corpus (LEC)**, a 2.4-million
word corpus of Multicultural London English compiled by Jenny Cheshire and
colleagues, accessed via [Sketch Engine](https://www.sketchengine.eu/london-english-corpus/).
Concordance search for the lemma "dead" returned 215 hits; all were retained.

## How to reproduce

1. Install dependencies:
   ```
   pip install anthropic pandas matplotlib openpyxl
   ```
2. Set your API key:
   ```
   export ANTHROPIC_API_KEY=sk-ant-...
   ```
3. Run classification:
   ```
   python classify.py
   ```

## Classification scheme

| Category | Description | Example |
|----------|-------------|---------|
| **LITERAL** | Actual death / non-functioning | *"my phone's gone dead"* |
| **INTENSIFIER** | Modifies adj/adv to mean "very" | *"dead lucky", "dead cheap"* |
| **EVALUATIVE** | Predicative, meaning "boring/lifeless" | *"the area's dead"* |

## AI use statement

Claude (Anthropic, claude-opus-4-7) was used to perform initial classification.
The exact prompt is reproduced in `classify.py`. All 215 outputs were manually
reviewed against the surrounding context. Five sentences (2.3%) remained
genuinely unclear and were excluded from analysis.
