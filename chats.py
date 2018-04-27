import html, os
import pandas as pd


class Chat:
	groupChat = False
	csvFileLocation = ".\\csv files\\message_file\\"

	def __init__(self, name, htmlfilename):
		self.chatName = name
		self.filename = htmlfilename
		self.imageCount = 0
		self.stickerCount = 0
		self.videoCount = 0
	
	def isGroupChat(self):
		return self.groupChat

	def setGroupChat(self):
		self.groupChat = True

	def setRawChat(self, raw):
		self.rawChat = raw

	def setParticipants(self, chatParticipants):
		self.participants = chatParticipants

	def getParticipants(self):
		return self.participants

	def setMessages(self, messages):
		self.messages = messages

	def getMessages(self):
		return self.messages

	def exportToCSV(self):
		if not os.path.exists(self.csvFileLocation):
			os.mkdir(self.csvFileLocation)
		self.messages
		fileName = html.unescape(self.chatName)
		fileName =  ''.join(e for e in fileName if e.isalnum())

		exportFile = self.csvFileLocation + fileName +'.csv'

		if not os.path.exists(exportFile):
			messageFrame = pd.DataFrame(self.messages)
			messageFrame.to_csv(exportFile)

	def getNumMessages(self):
		self.numMessages = len(self.messages)

		return(self.numMessages)

	def getNumImages(self):
		return self.imageCount
	
	def incrementImageCount(self):
		self.imageCount += 1

	def incrementStickerCount(self):
		self.stickerCount += 1

	def incrementVideoCount(self):
		self.videoCount += 1
	
	def getNumStickers(self):
		return self.stickerCount
