import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_weighted_average(file_path):
    df = preprocess_data(file_path)
    df = calculate_time_weights(df)

    # calculate weighted averages
    total_weight = df['CombinedWeight'].sum()
    harris_avg = np.average(df['Harris'], weights=df['CombinedWeight'])
    trump_avg = np.average(df['Trump'], weights=df['CombinedWeight'])

    return {
        'Harris': harris_avg,
        'Trump': trump_avg,
        'Harris_Trump_Difference': harris_avg - trump_avg,
        'Total_Weight': total_weight
    }

def preprocess_data(file_path):
    df = pd.read_csv(file_path)

    df['Sample'] = df['Sample'].str.split('@@').str[1].astype(float)
    df['EndDate'] = pd.to_datetime(df['Dates'].str.split('-').str[-1].str.split('@@').str[0].str.strip(), format='%m/%d')

    return df

def calculate_time_weights(df):
    most_recent_date = df['EndDate'].max()
    df['DaysSince'] = (most_recent_date - df['EndDate']).dt.days

    max_days = 30
    df['DateWeight'] = 1 - df['DaysSince'] / max_days
    df.loc[df['DateWeight'] < 0, 'DateWeight'] = 0

    df['CombinedWeight'] = df['Sample'] * df['DateWeight']

    return df

if __name__ == "__main__":
    file_path = "data/polls/Nat.csv"
    results = calculate_weighted_average(file_path)

    print("Time-Weighted Polling Average Results:")
    print(f"Harris: {results['Harris']:.2f}%")
    print(f"Trump: {results['Trump']:.2f}%")
    print(f"Difference (Harris - Trump): {results['Harris_Trump_Difference']:.2f}%")
    print(f"Total Combined Weight: {results['Total_Weight']:.2f}")
