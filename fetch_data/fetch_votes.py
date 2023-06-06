import requests
import json
import pandas as pd

# Define the URL and the query
url = "https://api.thegraph.com/subgraphs/name/nounsdao/nouns-subgraph"
query = """
query getVotes($skip: Int) {
  proposals(orderBy: createdBlock, first: 1000, skip: $skip) {
    id
    votes {
      blockNumber
      id
      support
      supportDetailed
      votes
      reason
    }
  }
}
"""

def fetch_data() -> dict:
    data = []
    skip = 0
    while True:
        response = requests.post(url, json={'query': query, 'variables': {'skip': skip}})
        new_data = response.json()['data']['proposals']
        if not new_data:
            break
        data.extend(new_data)
        skip += 1000
    return data

def save_data_to_csv_json(data: dict, filename_csv: str = '../data_raw/votes_raw.csv', filename_json: str = '../data_raw/votes_raw.json'):
    votes = []
    for proposal in data:
        for vote in proposal['votes']:
            vote['proposal_id'] = proposal['id']
            votes.append(vote)

    # Save to JSON
    with open(filename_json, 'w') as file:
        for index, vote in enumerate(votes):
            if index > 0:
                file.write('\n')  # Separate votes by a blank line
            json.dump(vote, file)

    # Save to CSV
    df = pd.DataFrame(votes)
    df.to_csv(filename_csv, index=False)

if __name__ == '__main__':
    data = fetch_data()
    save_data_to_csv_json(data)
    