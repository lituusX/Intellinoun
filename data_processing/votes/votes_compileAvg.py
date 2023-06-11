import pandas as pd

df = pd.read_csv('../../data/processed/votes_SentimentAnalysis_04.csv')

df = df[
    ['proposal_id', 'voterId', 'voteChoice', 'Sentiment Intensity', 'Sentiment Intensity_2', 'Sentiment Intensity_dv2',
     'Sentiment Intensity_dv3_r',
     'reason_formatted']].rename(
    columns={
        'proposal_id': 'Proposal ID',
        'voterId': 'Voter ID',
        'voteChoice': 'Vote',
        'Sentiment Intensity': 'Score A',
        'Sentiment Intensity_2': 'Score B',
        'Sentiment Intensity_dv2': 'Score C',
        'Sentiment Intensity_dv3_r': 'Score D',
        'reason_formatted': 'Reason',
    }
)

df.insert(df.columns.get_loc('Reason'), 'Score Avg', df[['Score A', 'Score B', 'Score C', 'Score D']].mean(axis=1))

df.to_csv('../../data/processed/datasets/votes_sentimentAVG.csv', index=False)
df.to_parquet('../../data/processed/datasets/votes_sentimentAVG.parquet', index=False)
