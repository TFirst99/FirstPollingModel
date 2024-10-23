import numpy as np
import pandas as pd
from typing import Dict, Any

def normalize(weights):
    return weights / np.sum(weights)

def sample_size_weight(df: pd.DataFrame, _: Dict[str, Any]) -> np.ndarray:
    return np.sqrt(df['Sample'])

def linear_time_weight(df: pd.DataFrame, params: Dict[str, Any]) -> np.ndarray:
    max_days = params.get('max_days', 30)
    most_recent_date = df['EndDate'].max()
    days_since = (most_recent_date - df['EndDate']).dt.days
    weight = 1 - days_since / max_days
    return np.maximum(weight, 0)

def exponential_time_weight(df: pd.DataFrame, params: Dict[str, Any]) -> np.ndarray:
    decay_rate = params.get('decay_rate', 0.1)
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

def combined_weight(df: pd.DataFrame, params: Dict[str, Any]) -> np.ndarray:
    sample_weights = normalize(sample_size_weight(df, params))
    time_weights = normalize(exponential_time_weight(df, params))
    quality_weights = normalize(pollster_quality_weight(df, params['ratings_df']))

    combined_weights = (
        params['sample_weight'] * sample_weights +
        params['time_weight'] * time_weights +
        params['quality_weight'] * quality_weights
    )

    return normalize(combined_weights)

def simple_average(df: pd.DataFrame, _: Dict[str, Any]) -> np.ndarray:
    return np.ones(len(df))

def calculate_weighted_average(df: pd.DataFrame, weighting_method: str, params: Dict[str, Any]) -> float:
    weighting_functions = {
        'sample_size': sample_size_weight,
        'linear_time': linear_time_weight,
        'exponential_time': exponential_time_weight,
        'pollster_quality': lambda df, p: pollster_quality_weight(df, p['ratings_df']),
        'combined': combined_weight,
        'simple_average': simple_average
    }

    if weighting_method not in weighting_functions:
        raise ValueError(f"Unknown weighting method: {weighting_method}")

    weights = weighting_functions[weighting_method](df, params)
    return np.average(df['Result'], weights=weights)
