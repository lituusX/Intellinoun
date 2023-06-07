import os
import openai
import csv
import json
import backoff
from openai.error import RateLimitError
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the OpenAI model to use
model = "text-davinci-003"

# Define CSV and JSON file paths
input_csv_path = "../../data_enhanced/votes_ReasonClassificationPrep.csv"
output_csv_path = "../../data_enhanced/votes_ReasonClassified.csv"
output_json_path = "../../data_enhanced/votes_ReasonClassified.json"

@backoff.on_exception(backoff.expo, RateLimitError, max_tries=5)
def call_openai_api(row):
    response = openai.Completion.create(
        model=model,
        prompt=f'Classify the sentiment in this sentence as positive, neutral, or negative: "{row["reason"]}"\nSentiment Classification:',
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response

def process_row(row):
    if row["reason"]:
        response = call_openai_api(row)

        # Add sentiment classification to row
        row["Sentiment Classification"] = response.choices[0].text.strip()

        # Add classification tokens to row
        row["Classification Tokens"] = response.usage["total_tokens"]

        return row

# Open input CSV file
with open(input_csv_path, "r") as input_csv:
    reader = csv.DictReader(input_csv)

    # Open output CSV file
    with open(output_csv_path, "w") as output_csv:
        fieldnames = reader.fieldnames + ["Sentiment Classification", "Classification Tokens"]
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()

        # Prepare an empty list to hold the JSON output data
        json_output_data = []

        # Create a ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Process rows in parallel
            futures = {executor.submit(process_row, row): row for row in reader}

            for future in as_completed(futures):
                row = futures[future]

                try:
                    # Get the result and write it to the output CSV
                    result = future.result()

                    if result is not None:
                        writer.writerow(result)

                        # Add the result to the JSON output data
                        json_output_data.append(result)

                except Exception as e:
                    print(f"An error occurred: {e}")

        # Write the JSON output data to file
        with open(output_json_path, 'w') as output_json:
            for entry in json_output_data:
                json.dump(entry, output_json, ensure_ascii=False)
                output_json.write('\n')
                