import os, re, html
import pandas as pd
from chats import Chat
from datetime import datetime

PARSE_ALL = "PARSE_ALL_FILES"


#parses HTML data and returns a list with Chat objects. Parse all HTML files by default
def parse(chats_to_parse = PARSE_ALL):

	#parse all files
	if chats_to_parse == PARSE_ALL:
		filesToParse = os.listdir()
	else:
		filesToParse = chats_to_parse.split(", ")
		

	chatNameStart = '<title>'
	chatNameEnd = "</title>" 
	messageStart = '<div class="_3-96 _2pio _2lek _2lel">'
	participantStart = '<div class="_1s7d">'
	htmlFiles = []
	chats = {}
	brokenFiles = []

	#get html files from folder
	for file in filesToParse:
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
			chatBeginIndex = rawChat.index(messageStart)
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
		chatBodyElements = rawChat[chatBeginIndex:].split(messageStart)
		# chatBodyElements = chatBodyElements[1:] #removes first empty string
		del chatBodyElements[-1]
		messages = []
		for rawMessage in chatBodyElements:
			#remove HTML tags and separate message data
			#add placeholders for media
			removedImg = re.sub('<img (.*)/>', 'some_image_was_here', rawMessage)
			stringCleanup = re.sub('<li>(.*)</li>', '', removedImg)
			stringCleanup = re.sub('<br />', '', stringCleanup)

			

			removedHTML = re.sub('<[^<]+?>', 'nonsense_to_remove', stringCleanup).split('nonsense_to_remove')
			
			messageData = list((filter(None, removedHTML))) #[date, sender, message]

			if len(messageData) == 0:
				# print(chatName, "no messages")
				# input()
				continue

			try:
				#handle if message and pic were sent in same message
				if messageData[2] == 'some_image_was_here' or "Download file" in messageData[2]:
					messageData[1] = messageData[1] + messageData[2]
					messageData[2] = messageData[3]
					newChat.incrementImageCount()		

				time = datetime.strptime(messageData[2], "%d %B %Y %H:%M")
				messages.append({'sender':messageData[0],'time':time, 'message':html.unescape(messageData[1])}) #convert HTML symbols

				if messageData[2] == 'some_image_was_here' and "messages/stickers" not in rawMessage:
					newChat.incrementImageCount()

				if "messages/stickers" in rawMessage:
					newChat.incrementStickerCount()					
			except:
				#sometimes deleted accounts mess up the array because "sender" is an empty string 
				#or message is empty because it doesn't show up on the exported data (e.g. waves, events)

				brokenFiles.append(file)
				# print(file, messageData)
				# input()
				pass
				
		messages.reverse() #set for chronological order
		newChat.setMessages(messages)
	return chats

if __name__ == "__main__":
	chatDict = parseAll()
	


