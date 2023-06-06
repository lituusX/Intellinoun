import requests
import json
import pandas as pd

# Define the URL and the new query
url = "https://api.thegraph.com/subgraphs/name/nounsdao/nouns-subgraph"
query = """
query getProposals($skip: Int) {
  proposals(orderBy: createdBlock, first: 1000, skip: $skip) {
    id
    title
    proposer {
      id
    }
    description
    status
    startBlock
    endBlock
    proposalThreshold
    quorumVotes
    executionETA
    quorumCoefficient
    minQuorumVotesBPS
    maxQuorumVotesBPS
    totalSupply
    forVotes
    againstVotes
    abstainVotes
    values
    targets
    signatures
    createdBlock
    createdTimestamp
    createdTransactionHash
    calldatas
  }
}
"""

def fetch_data() -> list:
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

proposals = fetch_data()

# Save all proposals to the same JSON and CSV files
filename_json = '../data_raw/proposals_raw.json'
filename_csv = '../data_raw/proposals_raw.csv'

# Save to JSON
with open(filename_json, 'w') as file:
    for index, proposal in enumerate(proposals):
        if index > 0:
            file.write('\n')  # Separate proposals by a blank line
        json.dump(proposal, file)

# Save to CSV
df = pd.json_normalize(proposals)
df.to_csv(filename_csv, index=False)
