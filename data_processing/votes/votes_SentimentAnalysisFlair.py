import csv
import json
import flair
from flair.models import TextClassifier
from flair.data import Sentence

input_csv_path = "../../data/enhanced/votes_SentimentAnalysis.csv"
output_csv_path = "../../data/enhanced/votes_SentimentAnalysis_flair.csv"
output_json_path = "../../data/enhanced/votes_SentimentAnalysis_flair.json"

classifier = TextClassifier.load('en-sentiment')


def process_row_flair(row):
    if row["reason"]:
        sentence = Sentence(row["reason"])
        classifier.predict(sentence)
        sentiment_result = sentence.labels[0]
        row["Sentiment Classification_flair"] = sentiment_result.value  # Sentiment value
        row["Sentiment Score_flair"] = sentiment_result.score  # Sentiment score
    return row


with open(input_csv_path, "r") as input_csv:
    reader = csv.DictReader(input_csv)

    with open(output_csv_path, "w", newline='') as output_csv:
        fieldnames = reader.fieldnames + ["Sentiment Classification_flair", "Sentiment Score_flair"]
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            updated_row = process_row_flair(row)
            writer.writerow(updated_row)

with open(output_csv_path, "r") as input_csv, open(output_json_path, "w") as output_json:
    reader = csv.DictReader(input_csv)
    data = [row for row in reader]
    json.dump(data, output_json)
