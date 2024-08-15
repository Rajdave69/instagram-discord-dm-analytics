import csv
import json
import os
import dateutil.parser


# instagram: ./instagram/.. .json
# discord ./discord.csv

# Load in and process the data
# discord first

with open('discord.csv', 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
    next(csv_reader)
    discord_data = [
        (line[1], int(dateutil.parser.parse(line[2]).timestamp()), line[3])
        for line in csv_reader
    ]
# AuthorID,Author,Date,Content,Attachments,Reactions
# author: 1, date: 2, content: 3

# instagram second
instagram_data = []

for item in os.listdir("./instagram"):
    if item.endswith(".json"):
        with open(f"./instagram/{item}", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)['messages']

            data = [
                (i['sender_name'], int(i['timestamp_ms'] / 1000), i['content'])
                for i in data
                if i.get('content') is not None and
                   not str(i.get('content')).endswith(
                       "wasn't notified about this message because they're in quiet mode.")
            ]

            instagram_data.extend(data)


print("Generating all graphs and stats")
from files import combined_hourly, userwise_daily, stats, combined_daily, appwise_daily

print()
combined_daily.combined_daily(discord_data, instagram_data)
appwise_daily.appwise_daily(discord_data, instagram_data)
userwise_daily.userwise_daily(discord_data, instagram_data)
combined_hourly.combined_hourly(discord_data, instagram_data)
stats.stats(discord_data, instagram_data)
print("\n\n")
print("Done")
print("type one of the following if you want to redo any one:")
print("combined_daily, appwise_daily, userwise_daily, combined_hourly, stats, all")

while True:

    match input():
        case "combined_daily":
            combined_daily.combined_daily(discord_data, instagram_data)
        case "appwise_daily":
            appwise_daily.appwise_daily(discord_data, instagram_data)
        case "userwise_daily":
            userwise_daily.userwise_daily(discord_data, instagram_data)
        case "combined_hourly":

            combined_hourly.combined_hourly(discord_data, instagram_data)
        case "stats":
            stats.stats(discord_data, instagram_data)
        case "all":
            combined_daily.combined_daily(discord_data, instagram_data)
            appwise_daily.appwise_daily(discord_data, instagram_data)
            userwise_daily.userwise_daily(discord_data, instagram_data)
            combined_hourly.combined_hourly(discord_data, instagram_data)
            stats.stats(discord_data, instagram_data)
        case _:
            break
