import numpy as np
import pandas as pd

def sample_size_weight(df: pd.DataFrame, _) -> np.ndarray:
    return np.sqrt(df['Sample'])

def linear_time_weight(df: pd.DataFrame, _, max_days: int = 30) -> np.ndarray:
    most_recent_date = df['EndDate'].max()
    days_since = (most_recent_date - df['EndDate']).dt.days
    weight = 1 - days_since / max_days
    return np.maximum(weight, 0)

def exponential_time_weight(df: pd.DataFrame, _, decay_rate: float = 0.1) -> np.ndarray:
    most_recent_date = df['EndDate'].max()
    days_since = (most_recent_date - df['EndDate']).dt.days
    return np.exp(-decay_rate * days_since)

def pollster_quality_weight(df: pd.DataFrame, ratings_df: pd.DataFrame) -> np.ndarray:
    weights = np.ones(len(df))
    for i, pollster in enumerate(df['Pollster']):
        rating = ratings_df.loc[ratings_df['Pollster'] == pollster, 'Grade'].iloc[0] if pollster in ratings_df['Pollster'].values else 'C'
        weight = {'A+': 5, 'A': 4, 'B': 3, 'C': 2, 'D': 1}.get(rating[0], 2)  # Default to C if not found
        weights[i] = weight
    return weights
