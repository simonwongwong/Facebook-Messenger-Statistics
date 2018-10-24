import json
import os
import pandas as pd
from datetime import datetime


def parse_from_json():
    """ Use this when the PWD contains all the JSON files with chat data and it will parse everything into two DataFrames.
        One to hold the data for each chat and one to hold all messages. These DataFrames will be returned  """

    all_files = [file for file in os.listdir() if file.endswith(".json")]

    chat_data = []
    chat_cols = ['participants', 'title', 'is_still_participant', 'thread_type', 'thread_path']
    message_data = []
    msg_cols = ['thread_path', 'timestamp', 'msg', 'sender', 'msg_type', 'sticker', 'photos', 'videos']

    for file in all_files:
        with open(file) as json_file:
            current_chat = json.load(json_file)

        participants = [x['name'] for x in current_chat.get('participants', '')]
        title = current_chat.get('title', '')
        is_still_participant = current_chat.get('is_still_participant', '')
        thread_type = current_chat.get('thread_type', '')
        thread_path = current_chat['thread_path']

        chat_data.append([participants, title, is_still_participant, thread_type, thread_path])

        for msg in current_chat['messages']:
            ts = msg.get('timestamp_ms', 0) // 1000
            body = msg.get('content', '')
            sender = msg.get('sender_name', '')
            msg_type = msg.get('type', '')
            sticker = msg.get('sticker', '')
            photos = msg.get('photos', '')
            videos = msg.get('videos', '')

            message_data.append([thread_path, ts, body, sender, msg_type, sticker, photos, videos])

    chat_df = pd.DataFrame(chat_data, columns=chat_cols)
    chat_df.set_index('thread_path', inplace=True)
    msg_df = pd.DataFrame(message_data, columns=msg_cols)
    msg_df['timestamp'] = msg_df['timestamp'].apply(datetime.fromtimestamp)

    return chat_df, msg_df


def load_from_csv():
    """ reads and returns DataFrame from persisted DataFrames in CSV format """
    chat_df = pd.read_csv("chat_df.csv", converters={"participants": eval})
    msg_df = pd.read_csv("msg_df.csv")
    msg_df['timestamp'] = pd.to_datetime(msg_df['timestamp'])

    return chat_df, msg_df


def persist(chat_df, msg_df):
    chat_df.to_csv("chat_df.csv")
    msg_df.to_csv("msg_df.csv")

    return True


if __name__ == "__main__":
    chat_df, msg_df = parse_from_json()
    print(chat_df)
    print(msg_df)
