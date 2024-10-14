import pandas as pd
import numpy as np


def calculate_weighted_average(file_path):
    # Read and preprocess the CSV file
    df = preprocess_data(file_path)

    # Calculate weighted average for Harris and Trump
    total_sample = df['Sample'].sum()
    harris_avg = np.average(df['Harris'], weights=df['Sample'])
    trump_avg = np.average(df['Trump'], weights=df['Sample'])

    return {
        'Harris': harris_avg,
        'Trump': trump_avg,
        'Harris_Trump_Difference': harris_avg - trump_avg,
        'Total_Sample': total_sample
    }

def preprocess_data(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Clean and convert the Sample column
    df['Sample'] = df['Sample'].str.split('@@').str[1].astype(float)

    return df

if __name__ == "__main__":
    file_path = "data/polls/Nat.csv"
    results = calculate_weighted_average(file_path)

    print("Simple Polling Average Results:")
    print(f"Harris: {results['Harris']:.2f}%")
    print(f"Trump: {results['Trump']:.2f}%")
    print(f"Difference (Harris - Trump): {results['Harris_Trump_Difference']:.2f}%")
    print(f"Total Sample Size: {results['Total_Sample']:.0f}")
