import pandas as pd
import json

def csv_to_json(filename_csv: str = 'data_raw/voteswithReason_raw.csv', filename_json: str = 'data_raw/voteswithReason_raw.json'):
    df = pd.read_csv(filename_csv)
    with open(filename_json, 'w') as f:
        for _, row in df.iterrows():
            json.dump(row.to_dict(), f)
            f.write("\n\n")

if __name__ == '__main__':
    csv_to_json()
