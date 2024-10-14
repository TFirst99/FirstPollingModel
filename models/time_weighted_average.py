import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_weighted_average(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Clean and convert the Sample column
    df['Sample'] = df['Sample'].str.split('@@').str[1].astype(float)

    # Convert Dates to datetime
    df['EndDate'] = pd.to_datetime(df['Dates'].str.split('-').str[-1].str.split('@@').str[0].str.strip(), format='%m/%d')

    # Calculate days since the most recent poll
    most_recent_date = df['EndDate'].max()
    df['DaysSince'] = (most_recent_date - df['EndDate']).dt.days

    # Calculate date weight (linear decay over 30 days)
    max_days = 30
    df['DateWeight'] = 1 - df['DaysSince'] / max_days
    df.loc[df['DateWeight'] < 0, 'DateWeight'] = 0

    # Combine sample size weight and date weight
    df['CombinedWeight'] = df['Sample'] * df['DateWeight']

    # Calculate weighted average for Harris and Trump
    total_weight = df['CombinedWeight'].sum()
    harris_avg = np.average(df['Harris'], weights=df['CombinedWeight'])
    trump_avg = np.average(df['Trump'], weights=df['CombinedWeight'])

    return {
        'Harris': harris_avg,
        'Trump': trump_avg,
        'Harris_Trump_Difference': harris_avg - trump_avg,
        'Total_Weight': total_weight
    }

if __name__ == "__main__":
    file_path = "data/polls/Nat.csv"
    results = calculate_weighted_average(file_path)

    print("Advanced Polling Average Results:")
    print(f"Harris: {results['Harris']:.2f}%")
    print(f"Trump: {results['Trump']:.2f}%")
    print(f"Difference (Harris - Trump): {results['Harris_Trump_Difference']:.2f}%")
    print(f"Total Combined Weight: {results['Total_Weight']:.2f}")
