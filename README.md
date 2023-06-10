# Intellinoun

[![CodeQL](https://github.com/lituusx/intellinoun/workflows/CodeQL/badge.svg)](https://github.com/lituusx/intellinoun/actions?query=workflow%3ACodeQL)

## Project Description

Intellinoun is a repository containing various scripts and datasets related to a language learning model (LLM) that
focuses on the analysis of text, with specific emphasis on noun usage. The project data is updated once every 24 hours.

## 🚧 WIP

### IN PROGRESS

- Sentiment Analysis
- Sentiment Reinforcement
- GUI to Generate Custom Datasets
- Dashboard for Research and Analysis

### PLANNED

- Proposal Data
- Auction Data
- Address and Transaction Tagging
- TBD

## What is Ensemble Learning

Ensemble learning is a machine learning paradigm where multiple models (often called "weak learners") are trained to
solve the same problem and combined to get better results. The main hypothesis is that when weak models are correctly
combined we can obtain more accurate and/or robust models. In our context, we are using two sentiment analysis models:
OpenAI's Davinci model and the NLTK's Vader SentimentIntensityAnalyzer. The first script uses the Davinci model for
sentiment classification and intensity prediction, while the second script uses Vader for a second round of sentiment
classification and intensity prediction. This helps us get more reliable results.

## Project Structure

The project's file structure has been updated and is now as follows:

```bash
.
├── LICENSE
├── README.md
├── convert_files
│   ├── __init__.py
│   └── csv_to_xlsx.py
├── data
│   ├── processed
│   │   ├── datasets
│   │   │   ├── votes_datasetSample.csv
│   │   │   └── votes_datasetSample.parquet
│   │   ├── votes_SentimentAnalysis.csv
│   │   ├── votes_SentimentAnalysis.json
│   │   ├── votes_SentimentAnalysis_02.csv
│   │   └── votes_SentimentAnalysis_02.json
│   ├── raw
│   │   ├── votes_raw.csv
│   │   ├── votes_raw.json
│   │   ├── votes_withReason.csv
│   │   └── votes_withReason.json
│   └── timestamps
│       └── fetch_votes.txt
├── data_processing
│   ├── __init__.py
│   └── votes
│       ├── __init__.py
│       ├── votes_SentimentAnalysis_01.py
│       ├── votes_SentimentAnalysis_02.py
│       └── votes_compileDataset.py
├── fetch_data
│   ├── __init__.py
│   └── votes_fetch.py
├── poetry.lock
├── pyproject.toml
└── tests
└── __init__.py
```

## New Scripts

Three new scripts `votes_SentimentAnalysis_01.py`, `votes_SentimentAnalysis_02.py`, and `votes_compileDataset.py` have
been added to the repository.

### Script 1: `votes_SentimentAnalysis_01.py`

This script does the following:

1. It first reads the input data from a CSV file.
2. For each row, if the row has a "reason", it performs grammar and spelling correction using the LanguageTool library.
3. It then splits the corrected text into chunks if the length is greater than the token limit. For each chunk, it calls
   the OpenAI API for sentiment classification and sentiment intensity prediction. The cost for each API call is also
   calculated and recorded.
4. The processed row data (including sentiment classification, intensity, tokens used, and cost) is then saved into an
   output CSV and JSON file.

### Script 2: `votes_SentimentAnalysis_02.py`

This script takes the output from the first script and performs another round of sentiment analysis using NLTK's Vader
SentimentIntensityAnalyzer. It does the following:

1. It first reads the output data from the first script from a CSV file.
2. For each row, it uses the Vader SentimentIntensityAnalyzer to analyze the sentiment of the text. This analyzer uses a
   combination of lexical heuristics and a valence score to determine the sentiment of the text.
3. The sentiment score from Vader (including positive, neutral, negative, and compound scores) is added to the row data.
4. The processed row data (including all data from the first script and the additional Vader sentiment scores) is then
   saved into a new output CSV and JSON file.

### Script 3: `votes_compileDataset.py`

This script reads the output from the second sentiment analysis script, compiles it into a single dataset, and saves the
dataset as both CSV and Parquet files in the `data/processed/datasets` directory.

These three scripts combined create an ensemble of two different sentiment analysis methods, which increases the
accuracy and reliability of the results.

## Execution

You can use the following commands to execute the scripts in the project:

```bash
poetry run python fetch_data/votes_fetch.py
poetry run python convert_files/csv_to_xlsx.py
poetry run python data_processing/votes/votes_SentimentAnalysis_01.py
poetry run python data_processing/votes/votes_SentimentAnalysis_02.py
poetry run python data_processing/votes/votes_compileDataset.py
```

The `fetch_data` script fetches the latest data, `convert_files` script is used for any file conversions if needed, and
the `data_processing` scripts perform sentiment analysis on the fetched data and compile the final dataset.

## Planned Work

- Work on sentiment reinforcement is currently underway. This will involve using the output from the sentiment analysis
  scripts to reinforce the sentiment prediction model.
- A GUI to generate custom datasets and a dashboard for research and analysis are also being developed.
- Future work includes extending the project to analyze other types of data such as proposal data and auction data, as
  well as tagging of addresses and transactions.

## Huggingface

Datasets can be found [here](https://huggingface.co/datasets/lituus/).

## License

This project is in the public domain. Check the [LICENSE](./LICENSE) file for more details.