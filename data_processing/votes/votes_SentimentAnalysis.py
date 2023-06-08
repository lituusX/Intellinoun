import os
import openai
import csv
import json
import backoff
import spacy
from openai.error import RateLimitError
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

os.environ["TOKENIZERS_PARALLELISM"] = "false"

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

model = "text-davinci-003"

nlp = spacy.load('en_core_web_trf')

input_csv_path = "../../data/prepared/votes_SentimentPrep.csv"
output_csv_path = "../../data/enhanced/votes_SentimentAnalysis.csv"
output_json_path = "../../data/enhanced/votes_SentimentAnalysis.json"

token_limit = 3000

cost_per_token = 0.02 / 1000


@backoff.on_exception(backoff.expo, RateLimitError, max_tries=5)
def call_openai_api(text, type):
    if type == "classification":
        prompt = f'Classify the sentiment in this sentence as positive, neutral, or negative: "{text}"\nSentiment Classification:'
    elif type == "rating":
        prompt = f'Rate the sentiment in this sentence on a scale from 1,2,3,4,5. With 1 being very negative and 5 very positive. Responde only with a numerical value: "{text}"\nSentiment rating:'

    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response


def process_row(row):
    if row["reason"]:
        doc = nlp(row["reason"])
        cleaned_text = " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
        row["reason_stripped"] = cleaned_text

        if len(cleaned_text) > token_limit:
            chunks = [cleaned_text[i:i + token_limit] for i in range(0, len(cleaned_text), token_limit)]
            for chunk in chunks:
                response = call_openai_api(chunk, "classification")
                row["Sentiment Classification"] = response.choices[0].text.strip()
                row["Classification Tokens"] = response.usage["total_tokens"]
                row["Classification Cost"] = response.usage["total_tokens"] * cost_per_token

                response = call_openai_api(chunk, "rating")
                row["Sentiment Rating"] = response.choices[0].text.strip()
                row["Rating Tokens"] = response.usage["total_tokens"]
                row["Sentiment Cost"] = response.usage["total_tokens"] * cost_per_token
        else:
            response = call_openai_api(cleaned_text, "classification")
            row["Sentiment Classification"] = response.choices[0].text.strip()
            row["Classification Tokens"] = response.usage["total_tokens"]
            row["Classification Cost"] = response.usage["total_tokens"] * cost_per_token

            response = call_openai_api(cleaned_text, "rating")
            row["Sentiment Rating"] = response.choices[0].text.strip()
            row["Rating Tokens"] = response.usage["total_tokens"]
            row["Sentiment Cost"] = response.usage["total_tokens"] * cost_per_token

        return row


with open(input_csv_path, "r") as input_csv:
    reader = csv.DictReader(input_csv)

    with open(output_csv_path, "w", newline='') as output_csv:
        fieldnames = reader.fieldnames + ["reason_stripped", "Sentiment Classification", "Classification Tokens",
                                          "Classification Cost", "Sentiment Rating", "Rating Tokens", "Sentiment Cost"]
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(process_row, row) for row in reader}
            for future in as_completed(futures):
                writer.writerow(future.result())

with open(output_csv_path, "r") as input_csv, open(output_json_path, "w") as output_json:
    reader = csv.DictReader(input_csv)
    data = [row for row in reader]
    json.dump(data, output_json)
