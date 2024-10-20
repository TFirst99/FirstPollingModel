# config.py

WEIGHTING_METHODS = {
    'sample_size': 'sample_size_weight',
    'linear_time': 'linear_time_weight',
    'exponential_time': 'exponential_time_weight',
    'pollster_quality': 'pollster_quality_weight',
    'combined': 'combined_weight',
    'simple_average': 'simple_average'
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

OUTPUT_PATH = 'polling_average.png'
