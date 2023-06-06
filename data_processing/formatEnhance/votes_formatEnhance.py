import pandas as pd
import json

def format_votes_csv(filename: str, output_filename: str):
    df = pd.read_csv(filename)
    df.rename(columns={'id': 'address'}, inplace=True)
    df['address'] = df['address'].apply(lambda x: x.split('-')[0] if '-' in x else x)
    df['casted_vote'] = df['supportDetailed'].map({1: "For", 0: "Against", 2: "Abstain"})
    df.to_csv(output_filename, index=False)

def format_votes_json(filename: str, output_filename: str):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            record = json.loads(line)
            if 'id' in record:
                record['address'] = record['id'].split('-')[0] if '-' in record['id'] else record['id']
                record.pop('id')
            if 'supportDetailed' in record:
                record['casted_vote'] = {1: "For", 0: "Against", 2: "Abstain"}.get(record['supportDetailed'])
            data.append(record)

    with open(output_filename, 'w') as f:
        for record in data:
            f.write(json.dumps(record))
            f.write('\n')

if __name__ == '__main__':
    # Apply to CSV
    format_votes_csv('../../data_raw/votes_raw.csv', '../../data_enhanced/votes_enhanced.csv')

    # Apply to JSON
    format_votes_json('../../data_raw/votes_raw.json', '../../data_enhanced/votes_enhanced.json')
    