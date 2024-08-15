from appwise_daily import prepare_data as appwise_prepare_data
from combined_daily import prepare_data as combined_prepare_data
import configparser

# Create configparser object
config_object = configparser.ConfigParser()
with open("../config.ini", "r") as file_object:
    config_object.read_file(file_object)
    user1_discord = config_object.get("user_1", "discord_name")
    user2_discord = config_object.get("user_2", "discord_name")

    user1_instagram = config_object.get("user_1", "instagram_name")
    user2_instagram = config_object.get("user_2", "instagram_name")


def stats(discord_data, instagram_data):
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

    prepared_appwise_data = appwise_prepare_data(discord_data, instagram_data)
    prepared_combined_data = combined_prepare_data(discord_data, instagram_data)

    combined_top_dates = most_active_date(prepared_combined_data)
    discord_top_dates = most_active_date(prepared_appwise_data[0])
    instagram_top_dates = most_active_date(prepared_appwise_data[1])

    from userwise_daily import prepare_data as prepare_combined_userwise_data
    prepared_combined_userwise_data = prepare_combined_userwise_data(discord_data, instagram_data)

    user1_top_dates = most_active_date(prepared_combined_userwise_data[0])

    user2_top_dates = most_active_date(prepared_combined_userwise_data[1])

    print(f"Most active date(s) (combined): {combined_top_dates[0]}, with {combined_top_dates[1]} messages.")
    print()
    print(f"Most active date(s) (discord): {discord_top_dates[0]}, with {discord_top_dates[1]} messages.")
    print(f"Most active date(s) (instagram): {instagram_top_dates[0]}, with {instagram_top_dates[1]} messages.")
    print()
    print(
        f"Most active date(s) ({user1_discord} / {user1_instagram}): {user1_top_dates[0]}, with {user1_top_dates[1]} messages.")
    print(
        f"Most active date(s) ({user2_discord} / {user2_instagram}): {user2_top_dates[0]}, with {user2_top_dates[1]} messages.")

    print('\n' * 2)

    combined_message_count = number_of_messages(prepared_combined_data)
    discord_message_count = number_of_messages(prepared_appwise_data[0])
    instagram_message_count = number_of_messages(prepared_appwise_data[1])
    user1_message_count = number_of_messages(prepared_combined_userwise_data[0])
    user2_message_count = number_of_messages(prepared_combined_userwise_data[1])

    print("No. of messages (combined): ", combined_message_count)
    print()
    print("No. of messages (discord): ", discord_message_count)
    print("No. of messages (instagram): ", instagram_message_count)
    print()
    print(f"No. of messages ({user1_discord} / {user1_instagram}): ", user1_message_count)
    print(f"No. of messages ({user2_discord} / {user2_instagram}): ", user2_message_count)

    print('\n' * 2)

    combined_character_count = number_of_characters(combined_data)
    discord_character_count = number_of_characters(discord_data)
    instagram_character_count = number_of_characters(instagram_data)
    user1_character_count = number_of_characters(user1_data)
    user2_character_count = number_of_characters(user2_data)
    print("No. of characters (combined): ", combined_character_count)
    print()
    print("No. of characters (discord): ", discord_character_count)
    print("No. of characters (instagram): ", instagram_character_count)
    print()
    print(f"No. of characters ({user1_discord} / {user1_instagram}): ", user1_character_count)
    print(f"No. of characters ({user2_discord} / {user2_instagram}): ", user2_character_count)

    print('\n' * 2)

    print("Avg message length (combined): ", average_message_length(combined_data, combined_character_count))
    print()
    print("Avg message length (discord): ", average_message_length(discord_data, discord_character_count))
    print("Avg message length (instagram): ", average_message_length(instagram_data, instagram_character_count))
    print()
    print(f"Avg message length ({user1_discord} / {user1_instagram}): ",
          average_message_length(user1_data, user1_character_count))
    print(f"Avg message length ({user2_discord} / {user2_instagram}): ",
          average_message_length(user2_data, user2_character_count))

    from combined_hourly import prepare_hourly_data
    most_active_hours, highest_message_count = most_active_hour(prepare_hourly_data(discord_data, instagram_data))
    print('\n' * 2)

    print(f"Most active hour(s): {most_active_hours}th hour with {highest_message_count} messages")


def most_active_date(data_tuple: tuple):
    dates, message_counts = data_tuple[0], data_tuple[1]

    # Find the highest message count and the corresponding dates in a single pass
    highest_message_count = max(message_counts)
    most_active_dates = [dates[i] for i, count in enumerate(message_counts) if count == highest_message_count]

    return most_active_dates, highest_message_count


def most_active_hour(data_tuple: tuple):
    hours, message_counts = data_tuple[0], data_tuple[1]

    # Find the highest message count and the corresponding dates in a single pass
    highest_message_count = max(message_counts)
    most_active_hours = [hours[i] for i, count in enumerate(message_counts) if count == highest_message_count]

    return most_active_hours, highest_message_count

def number_of_messages(data_tuple: tuple):
    return sum(data_tuple[1])


def number_of_characters(data: tuple):
    return sum([len(i[2]) for i in data])


def average_message_length(raw_data: tuple, character_count: int):
    # non-zero char messages/character_count

    num = 0
    for message in raw_data:
        if message[2] != '' or message[2] is not None:
            num += 1

    if num == 0:
        num = 1

    return character_count / num
