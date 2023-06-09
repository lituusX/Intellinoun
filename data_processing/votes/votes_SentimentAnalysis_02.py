import csv
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

input_csv_path = "../../data/processed/votes_SentimentAnalysis.csv"
output_csv_path = "../../data/processed/votes_SentimentAnalysis_02.csv"
output_json_path = "../../data/processed/votes_SentimentAnalysis_02.json"

sia = SentimentIntensityAnalyzer()


def get_sentiment(sentiment_scores):
    compound_score = sentiment_scores['compound']
    if compound_score >= 0.05:
        return "Positive", compound_score
    elif compound_score <= -0.05:
        return "Negative", compound_score
    else:
        return "Neutral", compound_score


def process_row_nltk(row):
    if row["reason"]:
        sentiment_scores = sia.polarity_scores(row["reason"])
        sentiment, score = get_sentiment(sentiment_scores)

        row["Sentiment Classification_2"] = sentiment
        row["Sentiment Intensity_2"] = score
    return row


with open(input_csv_path, "r") as input_csv:
    reader = csv.DictReader(input_csv)

    with open(output_csv_path, "w", newline='') as output_csv:
        fieldnames = reader.fieldnames + ["Sentiment Classification_2", "Sentiment Intensity_2"]
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            updated_row = process_row_nltk(row)
            writer.writerow(updated_row)

with open(output_csv_path, "r") as input_csv, open(output_json_path, "w") as output_json:
    reader = csv.DictReader(input_csv)
    data = [row for row in reader]
    json.dump(data, output_json)
