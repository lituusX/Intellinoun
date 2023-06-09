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


def transform_data(votes):
    for vote in votes:
        vote['voterId'] = vote['id'].split('-')[0]
        del vote['id']

        vote['voteChoice'] = "Abstain" if vote['supportDetailed'] == 2 else (
            "For" if vote['supportDetailed'] == 1 else "Against")

    return votes


def save_data_to_csv_json(data: dict, filename_csv: str = '../data/raw/votes_raw.csv',
                          filename_csv_with_reason: str = '../data/raw/votes_withReason.csv',
                          filename_json: str = '../data/raw/votes_raw.json',
                          filename_json_with_reason: str = '../data/raw/votes_withReason.json',
                          filename_timestamp: str = '../data/timestamps/fetch_votes.txt'):
    votes = []
    votes_with_reason = []
    highest_block_number = 0
    for proposal in data:
        transformed_votes = transform_data(proposal['votes'])
        for vote in transformed_votes:
            vote['proposal_id'] = proposal['id']
            votes.append(vote)
            if 'reason' in vote and vote['reason']:
                votes_with_reason.append(vote)
            if int(vote['blockNumber']) > highest_block_number:
                highest_block_number = int(vote['blockNumber'])

    # Save to JSON
    with open(filename_json, 'w') as file:
        for index, vote in enumerate(votes):
            if index > 0:
                file.write('\n')  # Separate votes by a blank line
            json.dump(vote, file)

    # Save to JSON with reason
    with open(filename_json_with_reason, 'w') as file:
        for index, vote in enumerate(votes_with_reason):
            if index > 0:
                file.write('\n')  # Separate votes by a blank line
            json.dump(vote, file)

    # Save to CSV
    df = pd.DataFrame(votes)
    df['blockNumber'] = df['blockNumber'].astype(int)
    df = df.sort_values('blockNumber')
    df.to_csv(filename_csv, index=False)

    # Save only rows where "reason" is not empty to a new CSV
    df_with_reason = pd.DataFrame(votes_with_reason)
    df_with_reason['blockNumber'] = df_with_reason['blockNumber'].astype(int)
    df_with_reason = df_with_reason.sort_values('blockNumber')
    df_with_reason.to_csv(filename_csv_with_reason, index=False)

    # Save the highest block number
    with open(filename_timestamp, "w") as file:
        file.write(str(highest_block_number))


if __name__ == '__main__':
    data = fetch_data()
    save_data_to_csv_json(data)
