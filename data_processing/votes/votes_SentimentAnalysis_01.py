import os
import openai
import csv
import json
import backoff
from openai.error import RateLimitError
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import language_tool_python

os.environ["TOKENIZERS_PARALLELISM"] = "false"

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

model = "text-davinci-003"

input_csv_path = "../../data/raw/votes_withReason.csv"
output_csv_path = "../../data/processed/votes_SentimentAnalysis.csv"
output_json_path = "../../data/processed/votes_SentimentAnalysis.json"

token_limit = 3000

cost_per_token = 0.02 / 1000

tool = language_tool_python.LanguageTool('en-US')


def correct_text(text, matches):
    current_offset = 0
    corrected_text = ""
    for match in matches:
        correction_offset_start = match.offset - current_offset
        correction_offset_end = correction_offset_start + match.errorLength
        corrected_text += text[:correction_offset_start]
        corrected_text += match.replacements[0] if len(match.replacements) > 0 else text[
                                                                                    correction_offset_start:correction_offset_end]
        text = text[correction_offset_end:]
        current_offset += match.errorLength
    corrected_text += text
    return corrected_text


@backoff.on_exception(backoff.expo, RateLimitError, max_tries=5)
def call_openai_api(text, type):
    if type == "classification":
        prompt = f'Classify the sentiment in this sentence as positive, neutral, or negative: "{text}"\nSentiment Classification:'
    elif type == "intensity":
        prompt = f'Rate the sentiment intensity in this sentence on a scale from -1 to 1. With -1 being very negative and 1 being very positive. Examples: "Very Positive" = 0.9224, "Neutral" = 0.0, "Slightly Positive" = 0.4215, "Slightly Negative" = -0.2354, "Very Negative" = -0.8670. Respond only with a numerical value: "{text}"\nSentiment Intensity:'

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
        matches = tool.check(row["reason"])
        corrected_text = correct_text(row["reason"], matches)
        row["reason_formatted"] = corrected_text

        if len(corrected_text) > token_limit:
            chunks = [corrected_text[i:i + token_limit] for i in range(0, len(corrected_text), token_limit)]
            for chunk in chunks:
                response = call_openai_api(chunk, "classification")
                row["Sentiment Classification"] = response.choices[0].text.strip()
                row["Classification Tokens"] = response.usage["total_tokens"]
                row["Classification Cost"] = response.usage["total_tokens"] * cost_per_token

                response = call_openai_api(chunk, "intensity")
                try:
                    row["Sentiment Intensity"] = float(response.choices[0].text.strip().split()[0])
                except ValueError:
                    print(f"Error: Unable to convert {response.choices[0].text.strip().split()[0]} to a float.")
                    row["Sentiment Intensity"] = None
                row["Intensity Tokens"] = response.usage["total_tokens"]
                row["Intensity Cost"] = response.usage["total_tokens"] * cost_per_token
        else:
            response = call_openai_api(corrected_text, "classification")
            row["Sentiment Classification"] = response.choices[0].text.strip()
            row["Classification Tokens"] = response.usage["total_tokens"]
            row["Classification Cost"] = response.usage["total_tokens"] * cost_per_token

            response = call_openai_api(corrected_text, "intensity")
            try:
                row["Sentiment Intensity"] = float(response.choices[0].text.strip().split()[0])
            except ValueError:
                print(f"Error: Unable to convert {response.choices[0].text.strip().split()[0]} to a float.")
                row["Sentiment Intensity"] = None
            row["Intensity Tokens"] = response.usage["total_tokens"]
            row["Intensity Cost"] = response.usage["total_tokens"] * cost_per_token
    return row


if __name__ == "__main__":
    with open(input_csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        with ThreadPoolExecutor(max_workers=8) as executor, \
                open(output_csv_path, 'w', newline='') as csv_outfile, \
                open(output_json_path, 'w') as json_outfile:

            csv_writer = csv.DictWriter(csv_outfile, fieldnames=None)
            futures = {executor.submit(process_row, row) for row in reader}
            results = []
            for future in as_completed(futures):
                result = future.result()
                if not csv_writer.fieldnames:
                    csv_writer.fieldnames = result.keys()
                    csv_writer.writeheader()
                csv_writer.writerow(result)
                results.append(result)
            json.dump(results, json_outfile, indent=4)
