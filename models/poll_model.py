import pandas as pd
from typing import Dict
from datetime import datetime

from models.data_loader import load_poll_data, load_pollster_ratings
from models.weighting_methods import calculate_weighted_average

class PollModel:
    def __init__(self, poll_file: str, ratings_file: str):
        self.poll_data = load_poll_data(poll_file)
        self.ratings_data = load_pollster_ratings(ratings_file)

    def run_model(self, end_date: pd.Timestamp, weighting_method: str, params: Dict) -> dict:
        df = self.poll_data[self.poll_data['EndDate'] <= end_date]

        harris_avg = calculate_weighted_average(df[['EndDate', 'Sample', 'Pollster', 'Harris']].rename(columns={'Harris': 'Result'}), weighting_method, params)
        trump_avg = calculate_weighted_average(df[['EndDate', 'Sample', 'Pollster', 'Trump']].rename(columns={'Trump': 'Result'}), weighting_method, params)

        return {
            'Harris': harris_avg,
            'Trump': trump_avg,
            'Harris_Trump_Difference': harris_avg - trump_avg,
        }

    def run_time_series(self, weighting_method: str, params: Dict) -> pd.DataFrame:
        date_range = pd.date_range(start=self.poll_data['EndDate'].min(), end=self.poll_data['EndDate'].max())
        results = []

        for date in date_range:
            result = self.run_model(date, weighting_method, params)
            result['Date'] = date
            results.append(result)

        return pd.DataFrame(results)
