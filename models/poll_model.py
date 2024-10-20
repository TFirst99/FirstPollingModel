import pandas as pd
import numpy as np
from typing import List, Callable
from datetime import datetime

from models.data_loader import load_poll_data, load_pollster_ratings

class PollModel:
    def __init__(self, poll_file: str, ratings_file: str):
        self.poll_data = load_poll_data(poll_file)
        self.ratings_data = load_pollster_ratings(ratings_file)

    def run_model(self, end_date: pd.Timestamp, weighting_methods: List[Callable]) -> dict:
        df = self.poll_data[self.poll_data['EndDate'] <= end_date]

        weights = np.ones(len(df))
        for method in weighting_methods:
            weights *= method(df, self.ratings_data)

        return self.weighted_average(df, weights)

    @staticmethod
    def weighted_average(df: pd.DataFrame, weights: np.ndarray) -> dict:
        total_weight = weights.sum()
        harris_avg = np.average(df['Harris'], weights=weights)
        trump_avg = np.average(df['Trump'], weights=weights)
        return {
            'Harris': harris_avg,
            'Trump': trump_avg,
            'Harris_Trump_Difference': harris_avg - trump_avg,
            'Total_Weight': total_weight
        }

    def run_time_series(self, weighting_methods: List[Callable]) -> pd.DataFrame:
        date_range = pd.date_range(start=self.poll_data['EndDate'].min(), end=self.poll_data['EndDate'].max())
        results = []

        for date in date_range:
            result = self.run_model(date, weighting_methods)
            result['Date'] = date
            results.append(result)

        return pd.DataFrame(results)
