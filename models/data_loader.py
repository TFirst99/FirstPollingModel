import pandas as pd
from datetime import datetime

def load_poll_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    df['EndDate'] = pd.to_datetime(df['end_date'], format='%m/%d/%y')
    cutoff_date = pd.to_datetime('2024-08-01')
    df = df[df['EndDate'] >= cutoff_date]
    df['Sample'] = pd.to_numeric(df['sample_size'], errors='coerce')
    df['state'] = df['state']
    df['pollscore'] = df['pollscore']

    vote_shares = df.pivot_table(
        index=['poll_id', 'EndDate', 'Sample', 'pollscore', 'state'],
        columns='candidate_name',
        values='pct',
        aggfunc='first'
    ).reset_index()

    final_df = vote_shares.rename(columns={
        'Kamala Harris': 'Harris',
        'Donald Trump': 'Trump'
    })

    final_df = final_df[['EndDate', 'Sample', 'Harris', 'Trump', 'pollscore', 'state']]
    final_df = pd.DataFrame(final_df.dropna())
    return final_df
