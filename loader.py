import json
import os
import pandas as pd
from datetime import datetime


CHATDF_FILENAME = "chat_df.csv"
MSGDF_FILENAME = "msg_df.csv"


def parse_from_json(path=None):
    """ Use this when the PWD contains all the JSON files with chat data and it will parse everything into two DataFrames.
        One to hold the data for each chat and one to hold all messages. These DataFrames will be returned  

        Pass in the path where your chat data was extracted using extract.py or leave empty to use current directory"""

    all_files = check_path(path, "json")

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


def load_from_csv(path=None):
    """ reads and returns DataFrame from persisted DataFrames in CSV format.
        Pass in a path to where the CSV files are located or leave blank to use current directory """
    chat_file = check_path(path, CHATDF_FILENAME)[0]
    msg_file = check_path(path, MSGDF_FILENAME)[0]

    chat_df = pd.read_csv(chat_file, converters={"participants": eval}, index_col='thread_path')
    msg_df = pd.read_csv(msg_file, index_col=0)
    msg_df['timestamp'] = pd.to_datetime(msg_df['timestamp'])

    return chat_df, msg_df


def persist(chat_df, msg_df):
    chat_df.to_csv(CHATDF_FILENAME)
    msg_df.to_csv(MSGDF_FILENAME)

    return True


def check_path(path, fmt):
    if path and not os.path.isdir(path):
        print("%s is not a valid directory" % path)
        raise NotADirectoryError

    filenames = os.listdir(path) if path else os.listdir()
    abs_path = os.path.abspath(path) if path else os.getcwd()
    matching_files = [abs_path + "\\" + file for file in filenames if file.lower().endswith(fmt)]

    if len(matching_files) == 0:
        print("No %s file found at %s" % (fmt, abs_path))
        raise FileNotFoundError

    return matching_files


if __name__ == "__main__":
    chat_df, msg_df = parse_from_json()
    print(chat_df)
    print(msg_df)
