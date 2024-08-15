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

    # Convert timestamps to datetime objects and count messages per day
    discord_message_count = defaultdict(int)
    for username, timestamp, message_content in discord_data:
        dt = datetime.fromtimestamp(timestamp)
        date_key = dt.date()
        discord_message_count[date_key] += 1

    instagram_message_count = defaultdict(int)
    for username, timestamp, message_content in instagram_data:
        dt = datetime.fromtimestamp(timestamp)
        date_key = dt.date()
        instagram_message_count[date_key] += 1

    # Create x-axis (dates) and y-axis (number of messages) lists
    _keys = [*discord_message_count.keys(), *instagram_message_count.keys()]
    start_date = min(_keys)
    end_date = max(_keys)

    # Fill in missing dates with 0 message counts
    full_dates = []

    full_discord_message_counts = []
    full_instagram_message_counts = []
    current_date = start_date
    while current_date <= end_date:
        full_dates.append(current_date)
        if current_date in discord_message_count:
            full_discord_message_counts.append(discord_message_count[current_date])
        else:
            full_discord_message_counts.append(0)
        if current_date in instagram_message_count:
            full_instagram_message_counts.append(instagram_message_count[current_date])
        else:
            full_instagram_message_counts.append(0)
        current_date += timedelta(days=1)

    # Convert full dates to dd/mm/yy
    full_dates = [i.strftime("%d/%m/%Y") for i in full_dates]

    return [
        (full_dates, full_discord_message_counts, 'Discord'),
        (full_dates, full_instagram_message_counts, 'Instagram'),
    ]


def appwise_daily(discord_data, instagram_data):
    print("e")
    data = prepare_data(discord_data, instagram_data)
    create_dynamic_linegraph(data, 'appwise_daily')
