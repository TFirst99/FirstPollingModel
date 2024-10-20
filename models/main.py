from models.data_loader import load_poll_data, load_pollster_ratings
from models.weighting_methods import sample_size_weight, linear_time_weight, exponential_time_weight, pollster_quality_weight
from models.averaging_methods import weighted_average
import numpy as np

def run_model(poll_file, ratings_file, weighting_methods):
    try:
        poll_data = load_poll_data(poll_file)
        ratings_data = load_pollster_ratings(ratings_file)

        weights = np.ones(len(poll_data))
        for method in weighting_methods:
            if method == 'sample_size':
                weights *= sample_size_weight(poll_data)
            elif method == 'linear_time':
                weights *= linear_time_weight(poll_data)
            elif method == 'exponential_time':
                weights *= exponential_time_weight(poll_data)
            elif method == 'pollster_quality':
                weights *= pollster_quality_weight(poll_data, ratings_data)
            else:
                print(f"Warning: Unknown weighting method '{method}'. Skipping.")

        results = weighted_average(poll_data, weights)
        return results
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def print_results(name, results):
    if results:
        print(f"\n{name} Results:")
        print(f"Harris: {results['Harris']:.2f}%")
        print(f"Trump: {results['Trump']:.2f}%")
        print(f"Difference (Harris - Trump): {results['Harris_Trump_Difference']:.2f}%")
        print(f"Total Combined Weight: {results['Total_Weight']:.2f}")
    else:
        print(f"\n{name} Results: Calculation failed.")

if __name__ == "__main__":
    poll_file = "models/data/polls/Nat.csv"
    ratings_file = "models/data/pollsterRatings.csv"

    # Sample-weighted average
    sample_weighted_results = run_model(poll_file, ratings_file, ['sample_size'])
    print_results("Sample-Weighted Polling Average", sample_weighted_results)

    # Linear time-weighted average
    linear_time_weighted_results = run_model(poll_file, ratings_file, ['linear_time'])
    print_results("Linear Time-Weighted Polling Average", linear_time_weighted_results)

    # Exponential time-weighted average
    exponential_time_weighted_results = run_model(poll_file, ratings_file, ['exponential_time'])
    print_results("Exponential Time-Weighted Polling Average", exponential_time_weighted_results)
