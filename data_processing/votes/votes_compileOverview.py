import pandas as pd

df = pd.read_csv('../../data/processed/votes_SentimentAnalysis_02.csv')

df = df[['proposal_id', 'voterId', 'voteChoice', 'Sentiment Intensity', 'Sentiment Intensity_2',
         'reason_formatted']].rename(
    columns={
        'proposal_id': 'Proposal ID',
        'voterId': 'Voter ID',
        'voteChoice': 'Vote',
        'Sentiment Intensity': 'Sentiment Score A',
        'Sentiment Intensity_2': 'Sentiment Score B',
        'reason_formatted': 'Reason',
    }
)

df.to_csv('../../data/processed/datasets/votes_reasonOverview.csv', index=False)
df.to_parquet('../../data/processed/datasets/votes_reasonOverview.parquet', index=False)
