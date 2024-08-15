import csv
import json
import dateutil.parser
from collections import defaultdict
from datetime import datetime, timedelta
import mplcyberpunk
from matplotlib import pyplot as plt
import matplotlib


def prepare_hourly_data(discord_data, instagram_data):
    all_data = [*discord_data, *instagram_data]

    # Convert timestamps to datetime objects and count messages per hour
    message_count = defaultdict(int)
    for username, timestamp, message_content in all_data:
        dt = datetime.utcfromtimestamp(timestamp)
        hour_key = dt.hour
        message_count[hour_key] += 1

    # Create x-axis (hours) and y-axis (number of messages) lists
    hours = list(range(24))
    message_counts = [message_count[hour] for hour in hours]

    return (hours, message_counts, 'Combined')


def combined_hourly(discord_data, instagram_data):
    data = prepare_hourly_data(discord_data, instagram_data)
    create_dynamic_bargraph([data])


# Plotting function for bar graph
def create_dynamic_bargraph(datasets):
    """
    Create a dynamic bar graph with multiple datasets.

    Parameters:
    - datasets: List of tuples where each tuple contains (hours, message_counts, label)
    """
    if not datasets:
        raise ValueError("At least one dataset is required")

    # Use the first dataset to determine the figure size
    hours, _, _ = datasets[0]
    num_hours = len(hours)
    fig_width = max(10, num_hours * 0.5)
    fig_height = max(10, 10)  # Keep height consistent for better visibility

    plt.style.use("cyberpunk")
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)

    bars = []
    bar_width = 0.35  # Width of the bars
    for i, (hours, message_counts, label) in enumerate(datasets):
        bars.append(ax.bar([h + i * bar_width for h in hours], message_counts, bar_width, label=label))

    # Set font size as a percentage of the figure width
    x_fontsize = max(10, fig_width * 0.015)
    y_fontsize = max(10, fig_height * 0.3)

    # Set ticks and their labels
    ax.set_xticks([h + bar_width * (len(datasets) - 1) / 2 for h in hours])
    ax.set_xticklabels(hours, rotation=90, fontsize=x_fontsize)
    ax.set_yticks(ax.get_yticks())
    ax.set_yticklabels(ax.get_yticks(), fontsize=y_fontsize)

    # Add padding to the bottom to prevent cutoff and reduce left/right padding
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.25)

    # Add legend
    ax.legend()

    # Make it look nicer
    for bar_set in bars:
        mplcyberpunk.add_bar_gradient(bars=bar_set)

    plt.savefig('./graphs/combined_hourly.png', dpi=100)


