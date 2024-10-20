import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_results(results, output_path):
    plt.figure(figsize=(15, 10))

    for name, df in results.items():
        plt.plot(df['Date'], df['Harris'], label=f'Harris ({name})')
        plt.plot(df['Date'], df['Trump'], label=f'Trump ({name})', linestyle='--')

    plt.title('Poll Results Over Time with Different Weighting Methods')
    plt.xlabel('Date')
    plt.ylabel('Poll Percentage')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
