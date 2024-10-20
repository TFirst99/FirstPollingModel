import numpy as np

def sample_size_weight(df):
    return np.sqrt(df['Sample'])

def linear_time_weight(df, max_days=30):
    most_recent_date = df['EndDate'].max()
    days_since = (most_recent_date - df['EndDate']).dt.days
    weight = 1 - days_since / max_days
    return np.maximum(weight, 0)

def exponential_time_weight(df, decay_rate=0.1):
    most_recent_date = df['EndDate'].max()
    days_since = (most_recent_date - df['EndDate']).dt.days
    weight = np.exp(-decay_rate * days_since)
    return weight

def pollster_quality_weight(df, ratings_df):
    return
