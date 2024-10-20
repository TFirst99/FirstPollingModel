import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_results(results, output_path):
    fig, axes = plt.subplots(3, 1, figsize=(15, 30))  # 3 rows, 1 column

    # plot for all Harris models
    ax = axes[0]
    for name, df in results.items():
        ax.plot(df['Date'], df['Harris'], label=f'{name}')
    ax.set_title('Harris Poll Results')
    ax.set_xlabel('Date')
    ax.set_ylabel('Poll Percentage')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # plot for all Trump models
    ax = axes[1]
    for name, df in results.items():
        ax.plot(df['Date'], df['Trump'], label=f'{name}')
    ax.set_title('Trump Poll Results')
    ax.set_xlabel('Date')
    ax.set_ylabel('Poll Percentage')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # combined weighting for trump vs. harris
    ax = axes[2]
    df = results['combined']
    ax.plot(df['Date'], df['Harris'], label='Harris (combined)', color='blue')
    ax.plot(df['Date'], df['Trump'], label='Trump (combined)', color='red', linestyle='--')
    ax.set_title('Trump vs Harris Combined Weighting')
    ax.set_xlabel('Date')
    ax.set_ylabel('Poll Percentage')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # save the plot
    for ax in axes:
        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_ha('right')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
