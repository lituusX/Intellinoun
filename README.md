# Intellinoun

## 🚧 WIP

Intellinoun is a repository containing various scripts and datasets for Nouns LLM. The project automatically updates data every 24 hours.

## Project Structure

```bash
.
├── LICENSE
├── README.md
├── convert_files
│   ├── __init__.py
│   └── csv_to_xlsx.py
├── data_embeddings
│   └── general_info_examples
│       └── nouns_lilnouns_sample.csv
├── data_enhanced
│   ├── proposals_detailed_enhanced.csv
│   ├── proposals_detailed_enhanced.json
│   ├── proposals_enhanced.csv
│   ├── proposals_enhanced.json
│   ├── votes_enhanced.csv
│   └── votes_enhanced.json
├── data_processing
│   └── formatEnhance
│       ├── proposals_addParticipation_rate.py
│       └── votes_formatEnhance.py
├── data_raw
│   ├── auctions_raw.csv
│   ├── auctions_raw.json
│   ├── enriched
│   │   ├── voteswithReason_Sentiment_raw.csv
│   │   ├── voteswithReason_Sentiment_raw.json
│   │   └── voteswithReason_Sentiment_raw.xlsx
│   ├── proposals_detailed_raw.csv
│   ├── proposals_detailed_raw.json
│   ├── proposals_raw.csv
│   ├── proposals_raw.json
│   ├── votes_raw.csv
│   └── votes_raw.json
├── fetch_data
│   ├── __init__.py
│   ├── fetch_auctions.py
│   ├── fetch_proposals.py
│   ├── fetch_proposals_detailed.py
│   └── fetch_votes.py
├── poetry.lock
├── pyproject.toml
└── tests
└── __init__.py
```

## File Descriptions

- [`LICENSE`](./LICENSE): The license file for the project.
- `README.md`: The file you are currently reading.
- `convert_files`:
- [`__init__.py`](./convert_files/__init__.py): Makes the directory a Python package.
- [`csv_to_xlsx.py`](./convert_files/csv_to_xlsx.py): Python script to convert CSV files to XLSX format.
- `data_raw`:
- `enriched`:
- [`voteswithReason_Sentiment_raw.csv`](./data_raw/enriched/voteswithReason_Sentiment_raw.csv): Raw, classified, rated, and sentiment analyzed voteswithReason data in CSV format.
- [`voteswithReason_Sentiment_raw.json`](./data_raw/enriched/voteswithReason_Sentiment_raw.json): Raw, classified, rated, and sentiment analyzed voteswithReason data in JSON format.
- [`voteswithReason_Sentiment_raw.xlsx`](./data_raw/enriched/voteswithReason_Sentiment_raw.xlsx): Raw, classified, rated, and sentiment analyzed voteswithReason data in XLSX format.
- [`proposals_detailed_raw.csv`](./data_raw/proposals_detailed_raw.csv): Detailed raw proposals data in CSV format.
- [`proposals_detailed_raw.json`](./data_raw/proposals_detailed_raw.json): Detailed raw proposals data in JSON format.
- [`proposals_raw.csv`](./data_raw/proposals_raw.csv): Raw proposals data in CSV format.
- [`proposals_raw.json`](./data_raw/proposals_raw.json): Raw proposals data in JSON format.
- [`votes_raw.csv`](./data_raw/votes_raw.csv): Raw votes data in CSV format.
- [`votes_raw.json`](./data_raw/votes_raw.json): Raw votes data in JSON format.
- `data_embeddings`:
- `general_info_examples`:
- [`nouns_lilnouns_sample.csv`](./data_embeddings/general_info_examples/nouns_lilnouns_sample.csv): Sample data containing general information examples for nouns and little nouns in CSV format.
- `data_enhanced`:
- [`proposals_detailed_enhanced.csv`](./data_enhanced/proposals_detailed_enhanced.csv): Enhanced proposals detailed data in CSV format.
- [`proposals_detailed_enhanced.json`](./data_enhanced/proposals_detailed_enhanced.json): Enhanced proposals detailed data in JSON format.
- [`proposals_enhanced.csv`](./data_enhanced/proposals_enhanced.csv): Enhanced proposals data in CSV format.
- [`proposals_enhanced.json`](./data_enhanced/proposals_enhanced.json): Enhanced proposals data in JSON format.
- [`votes_enhanced.csv`](./data_enhanced/votes_enhanced.csv): Enhanced votes data in CSV format.
- [`votes_enhanced.json`](./data_enhanced/votes_enhanced.json): Enhanced votes data in JSON format.
- `data_processing`:
- `formatEnhance`:
- [`proposals_addParticipation_rate.py`](./data_processing/formatEnhance/proposals_addParticipation_rate.py): Python script to add participation rate to proposals data.
- [`votes_formatEnhance.py`](./data_processing/formatEnhance/votes_formatEnhance.py): Python script to format and enhance votes data.
- `fetch_data`:
- [`__init__.py`](./fetch_data/__init__.py): Makes the directory a Python package.
- [`fetch_proposals.py`](./fetch_data/fetch_proposals.py): Python script to fetch proposal data.
- [`fetch_proposals_detailed.py`](./fetch_data/fetch_proposals_detailed.py): Python script to fetch detailed proposal data.
- [`fetch_votes.py`](./fetch_data/fetch_votes.py): Python script to fetch vote data.
- [`fetch_auctions.py`](./fetch_data/fetch_auctions.py): Python script to fetch auctions data.
- [`poetry.lock`](./poetry.lock): File generated by Poetry, a package and dependency management tool for Python. It ensures that the project's dependencies are consistent across different environments.
- [`pyproject.toml`](./pyproject.toml): File generated by Poetry for project configuration. It includes details about the project and its dependencies.
- `tests`:
- [`__init__.py`](./tests/__init__.py): Makes the directory a Python package.

## Pre-requisites

You will need the following installed on your machine before you can start using this project:

- Python 3.7 or later
- Poetry package manager

If you are using Windows, you can install Python via the [official website](https://www.python.org/downloads/windows/). If you are on a Mac, Python may already be installed. If not, you can use a package manager like brew to install Python.

For installing Poetry, it can be done through pip which is Python's package installer. Both Windows and Mac users can install Poetry by typing the following command in their command line interface:

```bash
pip install poetry
```

## Getting Started

To get the project up and running, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/lituusx/Intellinoun.git
```

2. Navigate into the directory:

```bash
cd Intellinoun
```

3. Install the dependencies using Poetry:

```bash
poetry install
```

4. Run the scripts:

```bash
poetry run python fetch_data/fetch_votes.py
poetry run python fetch_data/fetch_proposals.py
poetry run python fetch_data/fetch_proposals_detailed.py
poetry run python fetch_data/fetch_auctions.py
poetry run python convert_files/csv_to_xlsx.py
poetry run python data_processing/formatEnhance/votes_formatEnhance.py
poetry run python data_processing/formatEnhance/proposals_addParticipation_rate.py
```

## License

This project is in the public domain. Check the [LICENSE](./LICENSE) file for more details.
