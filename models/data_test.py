from data_loader import load_poll_data
from main import run_model

# Load all polls and filter for Pennsylvania
all_polls = load_poll_data('data/data.csv')
pa_polls = all_polls[all_polls['state'] == 'Pennsylvania']

# Print raw polling data
print("\nRaw Pennsylvania Polls:")
print(pa_polls.sort_values('EndDate')[['EndDate', 'Harris', 'Trump', 'Sample', 'pollscore']])

# Get model results
params = {'step_days': 1}
pa_results = run_model('data/data.csv', params, state='Pennsylvania')

print("\nModel Averages:")
print(pa_results.tail())
