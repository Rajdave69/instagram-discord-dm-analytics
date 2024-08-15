from create_dynamic_linegraph import create_dynamic_linegraph
import csv
import json
import dateutil.parser
from collections import defaultdict
from datetime import datetime, timedelta
import mplcyberpunk
from matplotlib import pyplot as plt
import matplotlib
# Import module
import configparser

# Create configparser object
config_object = configparser.ConfigParser()
with open("../config.ini", "r") as file_object:
    config_object.read_file(file_object)
    user1_discord = config_object.get("user_1", "discord_name")
    user2_discord = config_object.get("user_2", "discord_name")

    user1_instagram = config_object.get("user_1", "instagram_name")
    user2_instagram = config_object.get("user_2", "instagram_name")


def prepare_data(discord_data, instagram_data):
    combined_data = [*discord_data, *instagram_data]
    user1_data = [
        data for data in combined_data
        if data[0] == user1_discord or
           data[0] == user1_instagram
    ]

    user2_data = [
        data for data in combined_data
        if data[0] == user2_discord or
           data[0] == user2_instagram
    ]

    # Convert timestamps to datetime objects and count messages per day
    user1_message_count = defaultdict(int)
    for username, timestamp, message_content in user1_data:
        dt = datetime.fromtimestamp(timestamp)
        date_key = dt.date()
        user1_message_count[date_key] += 1

    user2_message_count = defaultdict(int)
    for username, timestamp, message_content in user2_data:
        dt = datetime.fromtimestamp(timestamp)
        date_key = dt.date()
        user2_message_count[date_key] += 1

    # Create x-axis (dates) and y-axis (number of messages) lists
    _keys = [*user1_message_count.keys(), *user2_message_count.keys()]
    start_date = min(_keys)
    end_date = max(_keys)

    # Fill in missing dates with 0 message counts
    full_dates = []

    full_user1_message_counts = []
    full_user2_message_counts = []
    current_date = start_date
    while current_date <= end_date:
        full_dates.append(current_date)
        if current_date in user1_message_count:
            full_user1_message_counts.append(user1_message_count[current_date])
        else:
            full_user1_message_counts.append(0)
        if current_date in user2_message_count:
            full_user2_message_counts.append(user2_message_count[current_date])
        else:
            full_user2_message_counts.append(0)
        current_date += timedelta(days=1)

    # Convert full dates to dd/mm/yy
    full_dates = [i.strftime("%d/%m/%Y") for i in full_dates]

    return [
        (full_dates, full_user1_message_counts, f"{user1_discord} / {user1_instagram}"),
        (full_dates, full_user2_message_counts, f"{user2_discord} / {user2_instagram}"),
    ]


def userwise_daily(discord_data, instagram_data):
    data = prepare_data(discord_data, instagram_data)
    create_dynamic_linegraph(data, 'userwise_daily')
