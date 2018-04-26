import os, shelve, message_parser, operator, html
from chats import Chat
import pandas as pd


def getMostMessaged(chat_dict, topNum):
	sizeDict = {}
	chatNames = list(chat_dict.keys())
	global totalMsg
	totalMsg = 0

	for chat in chatNames:
		num = chat_dict[chat].getNumMessages()
		totalMsg += num
		sizeDict[num] = chat
	sizes = list(sizeDict.keys())
	sizes.sort(key = int, reverse=True)

	top = sizes[:topNum]

	mostMessageList = []

	for i in range(0, len(top)):
		rank = i+1
		chat = html.unescape(sizeDict[top[i]])
		numMsg = top[i]
		mostMessageList.append({'rank':rank, 'chat':chat, 'number of messages': top[i], '% of total messages': top[i]*100/totalMsg})
	
	mostMessagedFrame = pd.DataFrame(mostMessageList)
	mostMessagedFrame.to_csv('.\\csv files\\most_messaged.csv')

	


def getMostImages(chat_dict, topNum):
	sizeDict = {}
	chatNames = list(chat_dict.keys())
	totalImages = 0

	for chat in chatNames:
		num = chat_dict[chat].getNumImages()
		totalImages += num
		sizeDict[num] = chat
	sizes = list(sizeDict.keys())
	sizes.sort(key = int, reverse=True)

	top = sizes[:topNum]
	mostImageList = []
	for i in range(0, len(top)):
		chat = html.unescape(sizeDict[top[i]])
		rank = i+1
		mostImageList.append({'rank':rank, 'chat':chat, 'number of images': top[i], '% of total images':top[i]*100/totalImages})
	
	mostImagesFrame = pd.DataFrame(mostImageList)
	mostImagesFrame.to_csv('.\\csv files\\most_images.csv')

def mostUsedWords(chat_dict, topNum, chars = 1):

	word_dict = {}

	for chat in chat_dict:
		chatObject = chat_dict[chat]
		for line in chatObject.messages:
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

	sorted_word_tuple = sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)
	sorted_dict = dict(sorted_word_tuple)

	mostWordsList = []

	for i in range(0, topNum):
		keys = list(sorted_dict.keys())
		rank = i+1
		num = sorted_dict[keys[i]]

		mostWordsList.append({'rank':rank, 'word':keys[i], 'number of uses':num, '% of total messages':num*100/totalMsg})

	mostWordsFrame = pd.DataFrame(mostWordsList)
	mostWordsFrame.to_csv('.\\csv files\\most_used_words.csv')


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

	sorted_time_tuple = sorted(timeDict.items(), key=operator.itemgetter(1), reverse=True)
	sorted_dict = dict(sorted_time_tuple)

	mostActiveTimeList = []
	
	if topNum == 'max':
		topNum = len(sorted_dict)

	for i in range(0, topNum):
		keys = list(sorted_dict.keys())
		rank = i+1
		num = sorted_dict[keys[i]]
		
		mostActiveTimeList.append({'rank':rank, typeOfTime:keys[i], 'number of messages':num, '% of total messages':num*100/totalMsg})

	activeTimeFrame = pd.DataFrame(mostActiveTimeList)
	filename = 'most_active_' + typeOfTime +'.csv'
	activeTimeFrame.to_csv('.\\csv files\\'+filename)

def exportCSV(array_of_dict):
	pass


if not os.path.exists('.\\csv files'):
	os.mkdir('.\\csv files\\')

chat_dict = message_parser.parseAll()
getMostMessaged(chat_dict, 20)
# getMostImages(chat_dict, 20)
mostUsedWords(chat_dict, 10, 10)
mostActiveTime(chat_dict, 'max', "time")
mostActiveTime(chat_dict, 24, "hour")
mostActiveTime(chat_dict, 60, "minute")
mostActiveTime(chat_dict, 12, "month")
mostActiveTime(chat_dict,'max', "year")
mostActiveTime(chat_dict,'max', "day")


