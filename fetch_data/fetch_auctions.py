import requests
import json
import pandas as pd

# Define the URL and the query
url = "https://api.thegraph.com/subgraphs/name/nounsdao/nouns-subgraph"
query = """
query getAuctions($skip: Int) {
  auctions(orderBy: endTime, first: 1000, skip: $skip) {
    id
    amount
    startTime
    endTime
    settled
    bidder {
      id
    }
  }
}
"""

def fetch_data() -> dict:
    data = []
    skip = 0
    while True:
        response = requests.post(url, json={'query': query, 'variables': {'skip': skip}})
        if response.status_code != 200:
            raise Exception(f"Request failed with status {response.status_code}")
        json_response = response.json()
        if 'data' not in json_response or 'auctions' not in json_response['data']:
            break
        new_data = json_response['data']['auctions']
        if not new_data:
            break
        data.extend(new_data)
        skip += 1000
    return data

def save_data_to_csv_json(data: dict, filename_csv: str = '../data_raw/auctions_raw.csv', filename_json: str = '../data_raw/auctions_raw.json'):
    auctions = data

    # Save to JSON
    with open(filename_json, 'w') as file:
        for index, auction in enumerate(auctions):
            if index > 0:
                file.write('\n')  # Separate auctions by a blank line
            json.dump(auction, file)

    # Save to CSV
    df = pd.DataFrame(auctions)
    df.to_csv(filename_csv, index=False)

if __name__ == '__main__':
    data = fetch_data()
    save_data_to_csv_json(data)
    