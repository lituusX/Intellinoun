import pandas as pd
import json

def add_participation_rate_csv(filename: str, output_filename: str):
    df = pd.read_csv(filename)
    df['voter_participation'] = (df['forVotes'] + df['againstVotes'] + df['abstainVotes']) / df['totalSupply'] * 100
    df.to_csv(output_filename, index=False)

def add_participation_rate_json(filename: str, output_filename: str):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            record = json.loads(line)
            record['voter_participation'] = (float(record['forVotes']) + float(record['againstVotes']) + float(record['abstainVotes'])) / float(record['totalSupply']) * 100
            data.append(record)

    with open(output_filename, 'w') as f:
        for record in data:
            f.write(json.dumps(record))
            f.write('\n')

if __name__ == '__main__':
    # Apply to CSV
    add_participation_rate_csv('../../data_raw/proposals_raw.csv', '../../data_enhanced/proposals_enhanced.csv')
    add_participation_rate_csv('../../data_raw/proposals_detailed_raw.csv', '../../data_enhanced/proposals_detailed_enhanced.csv')

    # Apply to JSON
    add_participation_rate_json('../../data_raw/proposals_raw.json', '../../data_enhanced/proposals_enhanced.json')
    add_participation_rate_json('../../data_raw/proposals_detailed_raw.json', '../../data_enhanced/proposals_detailed_enhanced.json')
    