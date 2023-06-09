import pandas as pd

df = pd.read_csv('../../data/processed/votes_SentimentAnalysis_02.csv')

df = df[['reason_formatted', 'Sentiment Classification', 'Sentiment Classification_2',
         'Sentiment Intensity', 'Sentiment Intensity_2']].rename(
    columns={
        'reason_formatted': 'reason',
        'Sentiment Classification': 'classification_a',
        'Sentiment Classification_2': 'classification_b',
        'Sentiment Intensity': 'intensity_a',
        'Sentiment Intensity_2': 'intensity_b'
    }
)

df['classification_match'] = df['classification_a'] == df['classification_b']
df['intensity_diff'] = df['intensity_a'] - df['intensity_b']

df.to_csv('../../data/processed/votes_Dataset.csv', index=False)
