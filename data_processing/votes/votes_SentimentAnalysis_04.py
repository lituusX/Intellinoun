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

input_csv_path = "../../data/processed/votes_SentimentAnalysis_03.csv"
output_csv_path = "../../data/processed/votes_SentimentAnalysis_04.csv"
output_json_path = "../../data/processed/votes_SentimentAnalysis_04.json"

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
def call_openai_api(text, vote_choice):
    prompt = f'This text represents a {vote_choice} vote in a Decentralized Autonomous Organization (DAO). Please analyze the sentiment expressed in the following statement, using a scale from -1 to 1, where -1 represents a very negative sentiment, 1 represents a very positive sentiment, and 0 represents a neutral sentiment. The sentiment should be evaluated within the context of reasons provided for the vote. Some examples include: "Very Positive" = 0.9224, "Neutral" = 0.0, "Slightly Positive" = 0.4215, "Slightly Negative" = -0.2354, "Very Negative" = -0.8670. Please respond solely with the numerical sentiment value for this statement: "{text}". \nCalculated Sentiment Value: '

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
        row["reason_formatted_dv3_r"] = corrected_text
        vote_choice = row["voteChoice"]

        if len(corrected_text) > token_limit:
            chunks = [corrected_text[i:i + token_limit] for i in range(0, len(corrected_text), token_limit)]
            for chunk in chunks:
                response = call_openai_api(chunk, vote_choice)
                try:
                    row["Sentiment Intensity_dv3_r"] = float(response.choices[0].text.strip().split()[0])
                except ValueError:
                    print(f"Error: Unable to convert {response.choices[0].text.strip().split()[0]} to a float.")
                    row["Sentiment Intensity_dv3_r"] = None
                row["Intensity Cost_dv3_r"] = response.usage["total_tokens"] * cost_per_token
        else:
            response = call_openai_api(corrected_text, vote_choice)
        try:
            row["Sentiment Intensity_dv3_r"] = float(response.choices[0].text.strip().split()[0])
        except ValueError:
            print(f"Error: Unable to convert {response.choices[0].text.strip().split()[0]} to a float.")
            row["Sentiment Intensity_dv3_r"] = None
        row["Intensity Tokens_dv3_r"] = response.usage["total_tokens"]
        row["Intensity Cost_dv3_r"] = response.usage["total_tokens"] * cost_per_token
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
