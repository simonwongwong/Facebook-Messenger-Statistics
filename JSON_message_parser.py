import os, re, json
import pandas as pd
from chats import Chat
from datetime import datetime
from dateutil import tz
import time as t

PARSE_ALL = "PARSE_ALL_FILES"



#parses JSON data and returns a list with Chat objects. Parse all JSON files by default
def parse(chats_to_parse = PARSE_ALL):

	#parse all files
	if chats_to_parse == PARSE_ALL:
		files_to_parse = os.listdir()
	else:
		files_to_parse = chats_to_parse.split(", ")

	chat_dict = {}
	totals = {}
	JSON_files = []
	total_messages = 0
	total_stickers = 0
	total_photos = 0
	total_videos = 0
	total_texts = 0

	#extract chat data
	for file in files_to_parse:
		if not file.endswith('json'):
			continue

		chat_data = json.load(open(file))

		try:
			chatName = chat_data['title']
		except KeyError:
			chatName = 'missing name (account deleted)'

		newChat = Chat(chatName, file)

		try:
			newChat.setParticipants(chat_data['participants'])
			newChat.setGroupChat()
		except:
			newChat.setParticipants('unable to find participants')

		messages = []

		for message in chat_data['messages']:
			total_messages += 1
			keys = list(message.keys())

			if 'sender_name' in keys:
				sender = message['sender_name']
			else:
				sender = 'missing name (account deleted)'
			if 'content' in keys:
				content = message['content']
				total_texts += 1
			if 'sticker' in keys:
				newChat.incrementStickerCount()
				total_stickers += 1
				continue
			if 'photos' in keys:
				newChat.incrementPhotoCount()
				total_photos += 1
				continue
			if "videos" in keys:
				newChat.incrementVideoCount()
				total_videos += 1
				continue


			#retrieve and convert time from UTC to local
			time = datetime.fromtimestamp(message['timestamp'])

			messages.append({'sender':sender, 'time':time,'message':content})

		messages.reverse()
		newChat.setMessages(messages)

		chat_dict[chatName] = newChat

	totals['total_messages'] = total_messages
	totals['total_stickers'] = total_stickers
	totals['total_photos'] = total_photos
	totals['total_videos'] = total_videos
	totals['total_texts'] = total_texts
	
	return chat_dict, totals

if __name__ == "__main__":
	chatDict = parse()
	


