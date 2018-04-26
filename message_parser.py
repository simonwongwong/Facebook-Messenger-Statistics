import os, re, html
import pandas as pd
from chats import Chat
from datetime import datetime

def parseAll():
	chatNameStart = '<title>'
	chatNameEnd = "</title>" 
	messageSplit = '</td></tr></tbody></table></div><div class="_3-94 _2lem">'
	messageStart = '<div class="_3-96 _2pio _2lek _2lel">'
	participantStart = '<div class="_1s7d">'
	allFiles = os.listdir()
	htmlFiles = []
	chats = {}
	brokenFiles = []

	#get html files from folder
	for file in allFiles:
		if file.endswith("html"):
			htmlFiles.append(file)

	#extract chat data
	for file in htmlFiles:
		rawChat = ""
		
		rawHtml = open(file, 'r', encoding="utf8")
		for line in rawHtml:
			rawChat += line
		rawHtml.close()	
		chatNameIndexStart = rawChat.index(chatNameStart) + len(chatNameStart)
		chatNameIndexEnd = chatNameIndexStart + rawChat[chatNameIndexStart:].index(chatNameEnd)
		chatName = html.unescape(rawChat[chatNameIndexStart:chatNameIndexEnd])

		# #create new chat object
		newChat = Chat(chatName, file)
		newChat.setRawChat(rawChat)

		try:
			chatBeginIndex = rawChat.index(messageSplit)
		except ValueError:
			rawChat = "no messages with " + chatName
			print("error:" + rawChat)
			continue

		chats[chatName] = newChat

		#find participants
		if participantStart in rawChat:
			participantIndex = rawChat.index(participantStart) + len(participantStart)
			participantsIndexEnd = rawChat[participantIndex:].index('</div>') + participantIndex
			participants = rawChat[participantIndex:participantsIndexEnd]
			newChat.setParticipants(participants)
			newChat.setGroupChat()


		#process chat data
		chatBodyElements = rawChat[chatBeginIndex:].split(messageSplit)
		chatBodyElements = chatBodyElements[1:] #removes first empty string
		del chatBodyElements[-1]
		messages = []
		for rawMessage in chatBodyElements:
			#remove HTML tags and separate message data
			#add placeholders for media
			removedImg = re.sub('<img (.*)/>', 'some_image_was_here', rawMessage)
			

			removedHTML = re.sub('<[^<]+?>', 'nonsense_to_remove', removedImg).split('nonsense_to_remove')
			messageData = list((filter(None, removedHTML))) #[date, sender, message]
			# messages.append(str(messageData) +"@@ raw: " +str(rawMessage) +"@@ rawer: " + str(removedHTML))
			try:
				time = datetime.strptime(messageData[0], "%d %B %Y %H:%M")
				messages.append({'sender':messageData[1],'time':time, 'message':html.unescape(messageData[2])}) #convert HTML symbols
				if messageData[2] == 'some_image_was_here' and "messages/stickers" not in rawMessage:
					newChat.incrementImageCount()
			except:
				#sometimes deleted accounts mess up the array because "sender" is an empty string
				pass
	# 
	# # 			brokenFiles.append(file)
				
		messages.reverse() #set for chronological order
		newChat.setMessages(messages)


	return chats

if __name__ == "__main__":
	chatDict = parseAll()
	# s = chatDict['Jay Shi']


