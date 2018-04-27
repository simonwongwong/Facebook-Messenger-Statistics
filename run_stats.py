import os, shelve, message_parser, operator, html
from chats import Chat
import pandas as pd


def sortDict(unsorted, topNum):
	sorted_dict = dict(sorted(unsorted.items(), key=operator.itemgetter(1), reverse=True))
	top_keys = list(sorted_dict.keys())[:topNum]
	return [sorted_dict, top_keys]

def exportDataFrame(top_list, filename):
	top_frame = pd.DataFrame(top_list)
	top_frame.to_csv('.\\csv files\\' + filename)	


def getMostMessaged(chat_dict, topNum):
	messageDict = {}
	chatNames = list(chat_dict.keys())
	global totalMsg
	totalMsg = 0

	for chat in chatNames:
		num = chat_dict[chat].getNumMessages()
		totalMsg += num
		messageDict[chat] = num

	
	sorted_dict, top_keys = sortDict(messageDict, topNum)

	mostMessagedList = []

	for i in range(0, len(top_keys)):
		rank = i+1
		chat = html.unescape(top_keys[i])
		numMsg = sorted_dict[chat]
		mostMessagedList.append({'rank':rank, 'chat':chat, 'number of messages': numMsg, '% of total messages': numMsg*100/totalMsg})
	
	exportDataFrame(mostMessagedList, 'most_messaged.csv')


def getMostImages(chat_dict, topNum):
	images_dict = {}
	chatNames = list(chat_dict.keys())
	totalImages = 0

	for chat in chatNames:
		num = chat_dict[chat].getNumImages()
		totalImages += num
		images_dict[chat] = num
	
	sorted_dict, top_keys = sortDict(images_dict, topNum)

	mostImageList = []

	for i in range(0, len(top_keys)):
		chat = html.unescape(top_keys[i])
		rank = i+1
		numImages = sorted_dict[chat]
		mostImageList.append({'rank':rank, 'chat':chat, 'number of images': numImages, '% of total images':numImages*100/totalImages})
	
	exportDataFrame(mostImageList, 'most_images_exchanged.csv')

def mostUsedWords(chat_dict, topNum, sender, chars = 1):

	word_dict = {}

	for chat in chat_dict:
		chatObject = chat_dict[chat]
		for line in chatObject.messages:
			if line['sender'] != sender:
				continue
			words = line['message'].split(" ")
			words = [x.lower() for x in words]
			for word in words:
				word = ''.join(e for e in word if e.isalnum())
				if word in word_dict:
					word_dict[word] += 1
				elif len(word) >= chars and "http" not in word:
					word_dict[word] = 1

	if "someimagewashere" in word_dict:
		del word_dict["someimagewashere"]

	sorted_dict, top_keys = sortDict(word_dict, topNum)

	mostWordsList = []

	for i in range(0, len(top_keys)):
		rank = i+1
		word = top_keys[i]
		num = sorted_dict[word]

		mostWordsList.append({'rank':rank, 'word':word, 'number of uses':num, '% of total messages':num*100/totalMsg})

	exportDataFrame(mostWordsList, 'most_used_words.csv')


def mostActiveTime(chat_dict, topNum, typeOfTime):
	timeDict = {}

	for chat in chat_dict:
		chatObject = chat_dict[chat]

		for message in chatObject.messages:
			datetime = message['time']

			if typeOfTime == "hour":
				time = datetime.hour
			elif typeOfTime == "time":
				time = str(datetime.hour) + ":" + str(datetime.minute)
			elif typeOfTime == "minute":
				time = datetime.minute
			elif typeOfTime == "year":
				time = datetime.year
			elif typeOfTime == "day":
				time = datetime.day
			elif typeOfTime == "month":
				time = datetime.strftime('%B')
			else:
				print("invalid type of time")
				return

			if time in timeDict:
				timeDict[time] += 1
			else:
				timeDict[time] = 1

	if topNum == 'max':
		topNum = len(timeDict)

	sorted_dict, top_keys = sortDict(timeDict, topNum)

	mostActiveTimeList = []
	

	for i in range(0, len(top_keys)):
		
		time_value = top_keys[i]
		rank = i+1
		num = sorted_dict[time_value]
		
		mostActiveTimeList.append({'rank':rank, typeOfTime:time_value, 'number of messages':num, '% of total messages':num*100/totalMsg})

	filename = 'most_active_' + typeOfTime +'.csv'
	exportDataFrame(mostActiveTimeList, filename)


if not os.path.exists('.\\csv files'):
	os.mkdir('.\\csv files\\')

chat_dict = message_parser.parse()
getMostMessaged(chat_dict, 20)
getMostImages(chat_dict, 20)
mostUsedWords(chat_dict, 10, 'Simon Wong', 5)
mostActiveTime(chat_dict, 'max', "time")
mostActiveTime(chat_dict, 'max', "hour")
mostActiveTime(chat_dict, 60, "minute")
mostActiveTime(chat_dict, 12, "month")
mostActiveTime(chat_dict,'max', "year")
mostActiveTime(chat_dict,'max', "day")


