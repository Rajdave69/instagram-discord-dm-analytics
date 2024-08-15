from create_dynamic_linegraph import create_dynamic_linegraph
import csv
import json
import dateutil.parser
from collections import defaultdict
from datetime import datetime, timedelta
import mplcyberpunk
from matplotlib import pyplot as plt
import matplotlib


def prepare_data(discord_data, instagram_data):
    all_data = [*discord_data, *instagram_data]
    print(len(all_data))

    # Convert timestamps to datetime objects and count messages per day
    message_count = defaultdict(int)
    for username, timestamp, message_content in all_data:
        dt = datetime.fromtimestamp(timestamp)
        date_key = dt.date()
        message_count[date_key] += 1

    # Create x-axis (dates) and y-axis (number of messages) lists
    start_date = min(message_count.keys())
    end_date = max(message_count.keys())
    dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    message_counts = [message_count[date] for date in dates]

    # Fill in missing dates with 0 message counts
    full_dates = []
    full_message_counts = []
    current_date = start_date
    while current_date <= end_date:
        full_dates.append(current_date)
        if current_date in message_count:
            full_message_counts.append(message_count[current_date])
        else:
            full_message_counts.append(0)
        current_date += timedelta(days=1)

    # Convert full dates to dd/mm/yy
    full_dates = [i.strftime("%d/%m/%Y") for i in full_dates]

    return (full_dates, full_message_counts, 'Combined')


def combined_daily(discord_data, instagram_data):
    print("e")
    data = prepare_data(discord_data, instagram_data)
    create_dynamic_linegraph([data], 'combined_daily')
