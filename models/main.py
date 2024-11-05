import pandas as pd
import numpy as np
from typing import Dict, Optional, Any
from datetime import datetime

class PollModel:
    def __init__(self, poll_data: pd.DataFrame):
        self.poll_data = poll_data

    def calculate_poll_weights(self, df: pd.DataFrame, current_date: datetime, params: Dict) -> np.ndarray:
        df = pd.DataFrame(df)

        days_since = (current_date - df['EndDate']).dt.total_seconds() / (24 * 60 * 60)

        sample_weights = np.sqrt(df['Sample'])
        time_weights = np.exp(-0.1 * days_since)

        min_score = df['pollscore'].min()
        max_score = df['pollscore'].max()
        normalized_pollscores = (df['pollscore'] - min_score) / (max_score - min_score)
        pollscore_weights = 1 + normalized_pollscores

        weights = sample_weights * time_weights * pollscore_weights

        total = np.sum(weights)
        if total > 0:
            weights = weights / total

        return weights

    def calculate_average(self, end_date: pd.Timestamp, params: Dict) -> Dict[str, float]:
        df = self.poll_data[self.poll_data['EndDate'] <= end_date].copy()

        if len(df) == 0:
            return {
                'Harris': float('nan'),
                'Trump': float('nan'),
                'Harris_Trump_Difference': float('nan')
            }

        weights = self.calculate_poll_weights(pd.DataFrame(df), end_date, params)

        harris_avg = float(np.average(df['Harris'], weights=weights))
        trump_avg = float(np.average(df['Trump'], weights=weights))

        return {
            'Harris': harris_avg,
            'Trump': trump_avg,
            'Harris_Trump_Difference': harris_avg - trump_avg
        }

    def run_time_series(self, params: Dict) -> pd.DataFrame:
        start_date = self.poll_data['EndDate'].min()
        end_date = self.poll_data['EndDate'].max()
        dates = pd.date_range(start=start_date, end=end_date, freq=f"{params['step_days']}D")

        results = []
        for date in dates:
            result = self.calculate_average(date, params)
            result['Date'] = date
            results.append(result)

        return pd.DataFrame(results)

def run_model(poll_file: str, params: Dict, state: Optional[str] = None):
    try:
        from data_loader import load_poll_data
        polls = load_poll_data(poll_file)

        if state is not None:
            polls = polls[polls['state'] == state]
            polls = pd.DataFrame(polls)

        if len(polls) == 0:
            print(f"No polling data available for {state} after August 1st, 2024")
            return None

        model = PollModel(polls)
        results = model.run_time_series(params)

        return results

    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    params = {
        'step_days': 1
    }

    from plotting import plot_state_results
    from data_loader import load_poll_data

    target_states = ['California', 'Pennsylvania', 'Texas']

    all_polls = load_poll_data('data/data.csv')

    for state in target_states:
        print(f"\nAnalyzing {state}:")
        state_polls = all_polls[all_polls['state'] == state]
        print(f"Number of polls for {state}: {len(state_polls)}")

        if len(state_polls) > 0:
            results = run_model(
                poll_file='data/data.csv',
                params=params,
                state=state
            )

            if results is not None:
                print(f"Creating plot for {state}")
                output_path = f'plots/{state}_polling.png'
                plot_state_results(state, results, output_path)
                print(f"Plot saved to {output_path}")
            else:
                print(f"No valid results for {state}")
        else:
            print(f"No polls found for {state}")
