import pandas as pd
import numpy as np
import re

def calculate_weighted_average(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Clean and convert the Sample column
    df['Sample'] = df['Sample'].apply(lambda x: re.search(r'(\d+)', str(x)).group(1) if re.search(r'(\d+)', str(x)) else None)
    df['Sample'] = pd.to_numeric(df['Sample'], errors='coerce')

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

if __name__ == "__main__":
    file_path = "data/polls/Nat.csv"
    results = calculate_weighted_average(file_path)

    print("Polling Average Results:")
    print(f"Harris: {results['Harris']:.2f}%")
    print(f"Trump: {results['Trump']:.2f}%")
    print(f"Difference (Harris - Trump): {results['Harris_Trump_Difference']:.2f}%")
    print(f"Total Sample Size: {results['Total_Sample']:.0f}")
