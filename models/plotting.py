import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_state_results(state_name, results_df, output_path):
    plt.figure(figsize=(12, 8))

    plt.plot(results_df['Date'], results_df['Harris'], label='Harris', color='blue')
    plt.plot(results_df['Date'], results_df['Trump'], label='Trump', color='red', linestyle='--')

    plt.title(f'Polling Average: {state_name}')
    plt.xlabel('Date')
    plt.ylabel('Poll Percentage')

    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()
