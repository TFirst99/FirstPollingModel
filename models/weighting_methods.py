import numpy as np
import pandas as pd
from typing import Dict, Any

def normalize_weights(weights: np.ndarray) -> np.ndarray:
    total = np.sum(weights)
    if total == 0:
        return np.zeros_like(weights)
    return weights / total

def sample_size_weight(df: pd.DataFrame, _: Dict[str, Any]) -> np.ndarray:
    weights = np.sqrt(df['Sample'])
    return normalize_weights(weights)

def linear_time_weight(df: pd.DataFrame, params: Dict[str, Any]) -> np.ndarray:
    max_days = params.get('max_days', 30)
    most_recent_date = df['EndDate'].max()
    days_since = (most_recent_date - df['EndDate']).dt.days
    weights = 1 - days_since / max_days
    weights = np.maximum(weights, 0)
    return normalize_weights(weights)

def exponential_time_weight(df: pd.DataFrame, params: Dict[str, Any]) -> np.ndarray:
    decay_rate = params.get('decay_rate', 0.1)
    most_recent_date = df['EndDate'].max()
    days_since = (most_recent_date - df['EndDate']).dt.days
    weights = np.exp(-decay_rate * days_since)
    return normalize_weights(weights)

def pollster_quality_weight(df: pd.DataFrame, ratings_df: pd.DataFrame) -> np.ndarray:
    grade_weights = {'A+': 5, 'A': 4, 'B': 3, 'C': 2, 'D': 1}
    default_weight = 2

    weights = np.ones(len(df))
    for i, pollster in enumerate(df['Pollster']):
        if pollster in ratings_df['Pollster'].values:
            grade = ratings_df.loc[ratings_df['Pollster'] == pollster, 'Grade'].iloc[0]
            weights[i] = grade_weights.get(grade[0] if grade else 'C', default_weight)
        else:
            weights[i] = default_weight

    return normalize_weights(weights)

def simple_average(df: pd.DataFrame, _: Dict[str, Any]) -> np.ndarray:
    weights = np.ones(len(df))
    return normalize_weights(weights)

def combined_weight(df: pd.DataFrame, params: Dict[str, Any]) -> np.ndarray:
    sample_weights = sample_size_weight(df, params)
    time_weights = exponential_time_weight(df, params)
    quality_weights = pollster_quality_weight(df, params['ratings_df'])

    combined_weights = (
        params['sample_weight'] * sample_weights +
        params['time_weight'] * time_weights +
        params['quality_weight'] * quality_weights
    )

    return normalize_weights(combined_weights)

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
