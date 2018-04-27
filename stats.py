import os, message_parser, operator, html
import matplotlib.pyplot as plt
from chats import Chat
import pandas as pd


def sortDict(unsorted, topNum):
	sorted_dict = dict(sorted(unsorted.items(), key=operator.itemgetter(1), reverse=True))
	top_keys = list(sorted_dict.keys())[:topNum]
	return [sorted_dict, top_keys]

def exportDataFrame(top_list, filename):
	top_frame = pd.DataFrame(top_list)
	top_frame.to_csv('.\\csv files\\' + filename)	
	return top_frame


def getMostMessaged(chat_dict, topNum):
	messageDict = {}
	chatNames = list(chat_dict.keys())
	allMsg = 0

	for chat in chatNames:
		num = chat_dict[chat].getNumMessages()
		allMsg += num
		messageDict[chat] = num

	
	sorted_dict, top_keys = sortDict(messageDict, topNum)

	mostMessagedList = []

	for i in range(0, len(top_keys)):
		rank = i+1
		chat = html.unescape(top_keys[i])
		numMsg = sorted_dict[chat]
		mostMessagedList.append({'rank':rank, 'chat':chat, 'number of messages': numMsg, '% of total messages': numMsg*100/allMsg})
	
	return exportDataFrame(mostMessagedList, 'most_messaged.csv')


def getMostImages(chat_dict, topNum):
	images_dict = {}
	chatNames = list(chat_dict.keys())
	allImages = 0


	for chat in chatNames:
		num = chat_dict[chat].getNumImages()
		allImages += num
		images_dict[chat] = num
	
	sorted_dict, top_keys = sortDict(images_dict, topNum)

	mostImageList = []

	for i in range(0, len(top_keys)):
		chat = html.unescape(top_keys[i])
		rank = i+1
		numImages = sorted_dict[chat]
		mostImageList.append({'rank':rank, 'chat':chat, 'number of images': numImages, '% of total images':numImages*100/allImages})
	
	return exportDataFrame(mostImageList, 'most_images_exchanged.csv')

def getMostUsedWords(chat_dict, topNum, sender, chars = 1):
	totalMessages = 0
	word_dict = {}

	for chat in chat_dict:
		chatObject = chat_dict[chat]
		for line in chatObject.messages:
			if line['sender'] != sender and sender != 'ANY_SENDER':
				continue

			totalMessages += 1

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

	if "videosomeimagewashere" in word_dict:
		del word_dict["videosomeimagewashere"]


	sorted_dict, top_keys = sortDict(word_dict, topNum)

	mostWordsList = []

	for i in range(0, len(top_keys)):
		rank = i+1
		word = top_keys[i]
		num = sorted_dict[word]

		mostWordsList.append({'rank':rank, 'word':word, 'number of uses':num, '% of total messages':num*100/totalMessages})

	return exportDataFrame(mostWordsList, 'most_used_words.csv')


def getMostActiveTime(chat_dict, topNum, typeOfTime):
	timeDict = {}
	totalMessages = 0

	for chat in chat_dict:
		chatObject = chat_dict[chat]

		for message in chatObject.messages:
			totalMessages += 1
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
		
		mostActiveTimeList.append({'rank':rank, typeOfTime:time_value, 'number of messages':num, '% of total messages':num*100/totalMessages})

	filename = 'most_active_' + typeOfTime +'.csv'
	return exportDataFrame(mostActiveTimeList, filename)

def plot(x,y, data, plot_title):
	plt.figure()
	plt.title(plot_title)
	plt.ylabel(y)
	plt.xlabel(x)

	x_label = data[x].tolist()
	x_data = range(len(x_label))
	y_data = data[y].tolist()

	plt.bar(x_data, y_data)
	plt.xticks(x_data, x_label, rotation='70')
	plt.show()


def typesOfMessages(chat_dict,sender):
	total = {}
	total['Messages'] = 0
	total['Stickers'] = 0

	word_dict = {}

	for chat in chat_dict:
		chatObject = chat_dict[chat]
		for line in chatObject.messages:
			if line['sender'] != sender and sender != 'ANY_SENDER':
				continue

			total['Messages'] += 1

			words = line['message'].split(" ")
			words = [x.lower() for x in words]
			for word in words:
				word = ''.join(e for e in word if e.isalnum())
				if word in word_dict:
					word_dict[word] += 1
				else:
					word_dict[word] = 1

		total['Stickers'] += chat_dict[chat].getNumStickers()

	if "someimagewashere" in word_dict:
		total['Images'] = word_dict['someimagewashere']
		del word_dict["someimagewashere"]

	if "videosomeimagewashere" in word_dict:
		total['Vids'] = word_dict["videosomeimagewashere"]
		del word_dict["videosomeimagewashere"]

	total['Text'] = total['Messages'] - total['Stickers'] - total['Images'] - total['Vids']

	type_list = []

	for type_msg in list(total.keys()):
		if type_msg != 'Messages':
			num = total[type_msg]
			type_list.append({'type of message':type_msg, 'number of messages':num, '% of total messages':num*100/total['Messages']})

	df_type_msg = exportDataFrame(type_list, 'type_of_message.csv')
	df_type_msg


	x = []
	x.append(total['Text'] / total['Messages'])
	x.append(total['Images'] / total['Messages'])
	x.append(total['Vids'] / total['Messages'])
	x.append(total['Stickers'] / total['Messages'])

	plt.figure()
	plt.title("Types of Messages Sent")

	patches, texts = plt.pie(x, startangle=90)
	plt.legend(patches, ['Text', 'Image', 'Video', 'Sticker'], loc="best")
	plt.tight_layout()
	plt.axis('equal')
	plt.show()







if __name__ == "__main__":
	if not os.path.exists('.\\csv files'):
		os.mkdir('.\\csv files\\')
	chat_dict = message_parser.parse()

	# getMostMessaged(chat_dict, 20)

	# getMostImages(chat_dict, 20)
	# getMostUsedWords(chat_dict, 10, 'Simon Wong', 5)
	# getMostActiveTime(chat_dict, 'max', "time")
	# getMostActiveTime(chat_dict, 'max', "hour")
	# getMostActiveTime(chat_dict, 60, "minute")
	# getMostActiveTime(chat_dict, 12, "month")
	# getMostActiveTime(chat_dict,'max', "year")
	# getMostActiveTime(chat_dict,'max', "day")


