import csv
import json
import dateutil.parser
from collections import defaultdict
from datetime import datetime, timedelta
import mplcyberpunk
from matplotlib import pyplot as plt
import matplotlib


def create_dynamic_linegraph(datasets, graph_name):
    """
    Create a dynamic line graph with multiple datasets.

    Parameters:
    - datasets: List of tuples where each tuple contains (full_dates, full_message_counts, label)
    - graph_name: Name of the graph to be saved
    """
    if not datasets:
        raise ValueError("At least one dataset is required")

    # Use the first dataset to determine the figure size
    full_dates, _, _ = datasets[0]
    num_dates = len(full_dates)
    fig_width = max(10, num_dates * 0.5)

    # Determine the number of y-axis labels for dynamic height adjustment
    y_values = [full_message_counts for _, full_message_counts, _ in datasets]
    flat_y_values = [item for sublist in y_values for item in sublist]
    num_y_labels = len(set(flat_y_values))
    fig_height = min(max(10, num_y_labels * 0.5), 20)  # Set a reasonable maximum height

    plt.style.use("cyberpunk")
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)

    # Plot each dataset
    for full_dates, full_message_counts, label in datasets:
        ax.plot(full_dates, full_message_counts, marker='o', label=label)

    # Set font size as a percentage of the figure width and height
    x_fontsize = max(25, fig_width * 0.1)
    y_fontsize = max(50, fig_height * 0.5)

    # Set ticks and their labels
    ax.set_xticks(range(num_dates))
    ax.set_xticklabels(full_dates, rotation=90, fontsize=x_fontsize)
    ax.set_yticks(ax.get_yticks())
    ax.set_yticklabels(ax.get_yticks(), fontsize=y_fontsize)

    # Add padding to the bottom to prevent cutoff and reduce left/right padding
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.25)

    # Add legend
    ax.legend()

    # Make it look nicer
    mplcyberpunk.add_glow_effects()

    plt.savefig(f'./graphs/{graph_name}.png', dpi=100)


# Example usage
discord_data = [
    # Replace with your data
    # Example: ('username1', 1625097600, 'message1'),
]

instagram_data = [
    # Replace with your data
    # Example: ('username2', 1625097600, 'message2'),
]

# Assuming data is prepared
# datasets = prepare_data(discord_data, instagram_data)
# create_dynamic_linegraph(datasets, 'combined_daily')
