import os, JSON_message_parser, operator
import matplotlib.pyplot as plt
from chats import Chat
import pandas as pd

fake_names = ['Kanye West', "King T'Challa", 'Tim Horton', 'Elon Musk', 'Ira Glass', 'Simon Wong', 'Mark Zuckerberg', 'Queen Elizabeth', 'Beyonce', 'Spongebob Squarepants']

def setTotals(total_dict):
	global totals
	totals = total_dict

def sortDict(unsorted, topNum, reverse_sort=True):
	sorted_dict = dict(sorted(unsorted.items(), key=operator.itemgetter(1), reverse=reverse_sort))
	top_keys = list(sorted_dict.keys())[:topNum]
	return [sorted_dict, top_keys]

def exportDataFrame(top_list, filename):
	top_frame = pd.DataFrame(top_list)
	top_frame.to_csv('.\\csv files\\' + filename)	
	return top_frame

def getAverageMessageLength(chat_dict, topNum, chats_to_analyze, typeLen='words'):
	message_length = {}
	average_length = {}

	for chat_name in chats_to_analyze:
		chat = chat_dict[chat_name]

		for message_data in chat.getMessages():
			sender = message_data['sender']

			if sender == 'missing name (account deleted)':
				continue

			if typeLen == 'words':
				words = message_data['message'].split(" ")
				length = len(words)
			elif typeLen == 'chars':
				length = len(message_data['message'])

			if sender in list(message_length.keys()):
				message_length[sender]['total_len'] += length
				message_length[sender]['num_msg'] += 1
			else:
				message_length[sender] = {}
				message_length[sender]['total_len'] = length
				message_length[sender]['num_msg'] = 1

	for sender in message_length:
		data = message_length[sender]
		average_length[sender] = data['total_len']/data['num_msg']

	sorted_dict, top_keys = sortDict(average_length, topNum)

	average_message_length = []

	for i in range(0, len(top_keys)):
		rank = i+1
		sender = top_keys[i]
		length = sorted_dict[sender]
		average_message_length.append({'rank':rank, 'sender':sender, 'average message length': length})
	
	return exportDataFrame(average_message_length, 'average_message_length.csv')


def inMostGroupChats(chat_dict, topNum):
	person = {}
	numGroupChats = 0

	for chat_name in chat_dict:
		chat = chat_dict[chat_name]
		if chat.isGroupChat():
			participants = chat.getParticipants()
			numGroupChats += 1
		else:
			continue

		for participant in participants:

			if participants == "unable to find participants":
				break

			if participant in list(person.keys()):
				person[participant] += 1
			else:
				person[participant] = 1

	sorted_dict, top_keys = sortDict(person, topNum)
	most_common_participant = []

	for i in range(0, len(top_keys)):
		rank = i+1
		participant = top_keys[i]
		numChats = sorted_dict[participant]
		most_common_participant.append({'rank':rank, 'participant':participant, 'number of group chats': numChats, '% of total chats': numChats*100/numGroupChats})
	
	return exportDataFrame(most_common_participant, 'most_common_participant.csv')


	

def getMostMessaged(chat_dict, topNum):
	message_dict = {}
	chatNames = list(chat_dict.keys())

	for chat in chatNames:
		num = chat_dict[chat].getNumMessages()
		message_dict[chat] = num

	
	sorted_dict, top_keys = sortDict(message_dict, topNum)

	most_messaged = []

	for i in range(0, len(top_keys)):
		rank = i+1
		chat = top_keys[i]
		numMsg = sorted_dict[chat]
		most_messaged.append({'rank':rank, 'chat':chat, 'number of messages': numMsg, '% of total messages': numMsg*100/totals['total_messages']})
	
	return exportDataFrame(most_messaged, 'most_messaged.csv')


def getMostUsedWords(chat_dict, topNum, sender, chars = 1):
	word_dict = {}

	for chat in chat_dict:
		chat_object = chat_dict[chat]

		for message_data in chat_object.getMessages():
			if message_data['sender'] != sender and sender != 'ANY_SENDER':
				continue

			words = message_data['message'].split(" ")
			words = [x.lower() for x in words]

			for word in words:
				word = ''.join(letter for letter in word if letter.isalnum())

				if word in word_dict:
					word_dict[word] += 1

				elif len(word) >= chars and "http" not in word:
					word_dict[word] = 1


	sorted_dict, top_keys = sortDict(word_dict, topNum)

	mostWordsList = []

	for i in range(0, len(top_keys)):
		rank = i+1
		word = top_keys[i]
		num = sorted_dict[word]

		mostWordsList.append({'rank':rank, 'word':word, 'number of uses':num, '% of total messages':num*100/totals['total_messages']})

	return exportDataFrame(mostWordsList, 'most_used_words.csv')


def getMostActiveTime(chat_dict, topNum, typeOfTime):
	time_dict = {}

	for chat in chat_dict:
		chat_object = chat_dict[chat]

		for message in chat_object.getMessages():

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

			if time in time_dict:
				time_dict[time] += 1
			else:
				time_dict[time] = 1

	if topNum == 'max':
		topNum = len(time_dict)

	sorted_dict, top_keys = sortDict(time_dict, topNum)

	most_active_time = []
	

	for i in range(0, len(top_keys)):
		
		time_value = top_keys[i]
		rank = i+1
		num = sorted_dict[time_value]
		
		most_active_time.append({'rank':rank, typeOfTime:time_value, 'number of messages':num, '% of total messages':num*100/totals['total_messages']})

	filename = 'most_active_' + typeOfTime +'.csv'
	return exportDataFrame(most_active_time, filename)

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


def typesOfMessages(chat_dict, chat_to_analyze='ANY_CHAT'):
	if chat_to_analyze == 'ANY_CHAT':
		chats = list(chat_dict.keys())
	else:
		chats = [chat_to_analyze]

	total = {'messages':0,'stickers':0,'photos':0,'videos':0}
	percent = {'stickers':0,'photos':0,'videos':0}


	for chat in chats:
		total['messages'] += chat_dict[chat].getNumMessages()
		total['stickers'] += chat_dict[chat].getNumStickers()
		total['photos'] += chat_dict[chat].getNumPhotos()
		total['videos'] += chat_dict[chat].getNumVideos() 
	
	total['text'] = total['messages'] - total['stickers'] - total['photos'] - total['videos']

	type_list = []

	for type_msg in list(total.keys()):
		if type_msg != 'messages':
			num = total[type_msg]
			percent[type_msg] = num*100/total['messages']
			type_list.append({'type of message':type_msg, 'number of messages':num, '% of total messages':percent[type_msg]})

	df_type_msg = exportDataFrame(type_list, 'type_of_message.csv')
	


	x = []
	x.append(percent['text'])
	x.append(percent['photos'])
	x.append(percent['videos'])
	x.append(percent['stickers'])

	plt.figure()
	plt.title("Types of Messages Sent")

	patches, texts = plt.pie(x, startangle=90)
	plt.legend(patches, ['Text', 'Photo', 'Video', 'Sticker'], loc="best")
	plt.tight_layout()
	plt.axis('equal')
	plt.show()

	return df_type_msg

def chatImbalance(chat_dict, chats_to_analyze):
	data = {}
	imbalance = {}
	total_received = 0
	total_sent = 0

	for chat_name in chats_to_analyze:
		chat = chat_dict[chat_name]
		#only look at non-group chats, otherwise imbalance will always fall on group chats
		if chat.isGroupChat(): 
			continue

		data[chat_name] = {'received_messages':0, 'chat_total':chat.getNumMessages()}
		messages = chat.getMessages()

		for message_data in messages:
			if message_data['sender'] == chat_name:
				data[chat_name]['received_messages'] += 1
				total_received += 1
			else: 
				total_sent += 1

		imbalance[chat_name] = (data[chat_name]['received_messages'] * 100) / data[chat_name]['chat_total']

	sorted_dict, top_keys = sortDict(imbalance, len(imbalance), reverse_sort=False)
	most_imbalanced = []

	for i in range(0, len(top_keys)):
		rank = i+1
		chat = top_keys[i]
		imbal = sorted_dict[chat]
		most_imbalanced.append({'rank':rank, 'chat':chat, '% of messages were received': imbal})
		
	return exportDataFrame(most_imbalanced, 'most_imbalanced.csv')	




if __name__ == "__main__":
	if not os.path.exists('.\\csv files'):
		os.mkdir('.\\csv files\\')
	chat_dict, totals = JSON_message_parser.parse()

	# getMostMessaged(chat_dict, 20)

	# getMostImages(chat_dict, 20)
	# getMostUsedWords(chat_dict, 10, 'Simon Wong', 5)
	# getMostActiveTime(chat_dict, 'max', "time")
	# getMostActiveTime(chat_dict, 'max', "hour")
	# getMostActiveTime(chat_dict, 60, "minute")
	# getMostActiveTime(chat_dict, 12, "month")
	# getMostActiveTime(chat_dict,'max', "year")
	# getMostActiveTime(chat_dict,'max', "day")


