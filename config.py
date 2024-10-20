# config.py

WEIGHTING_METHODS = {
    'Sample Size': 'sample_size_weight',
    'Linear Time': 'linear_time_weight',
    'Exponential Time': 'exponential_time_weight',
    'Pollster Quality': 'pollster_quality_weight'
}

TIME_WEIGHTING = {
    'linear_max_days': 30,
    'exponential_decay_rate': 0.1
}

POLLSTER_QUALITY_GRADES = {
    'A+': 5,
    'A': 4,
    'B': 3,
    'C': 2,
    'D': 1
}

DEFAULT_POLLSTER_GRADE = 'C'

DATA_PATHS = {
    'polls': 'data/polls/Nat.csv',
    'pollster_ratings': 'data/pollsterRatings.csv'
}

OUTPUT_PATH = 'poll_results_comparison.png'
