import ika
from PodSixNet.Connection import ConnectionListener, connection
from data import data

import window, subwindow
import text

class ChatBox(ConnectionListener, subwindow.Subwindow): 
	
	def __init__(self):
		self.font = data.fonts["system"]
		self.maxLines = 10 #number of lines that can be displayed at any one time.
				
		##set numbers are temp
		self.x = 5
		self.y = 470
		self.width = 400
		self.height = (self.maxLines+1)*(self.font.height+2)
		self.id = 'chatbox'
		
		subwindow.Subwindow.__init__(self, self.width, self.height, self.id)
		window.NewWindow(self, self.x, self.y, self.width, self.height, self.id)
		
		self.lines = [] #currently displayed lines
		
		self.slots['text input'] = text.InputBox(0, self.height - self.font.height - 4, self.width-4, onEnter = self.SendText)
		
		
	def AddLine(self, text):
		"""
			Adds a single line of text to the chat box
		"""
		
		self.lines.append(text)
		
		if len(self.lines) > self.maxLines:
			self.lines.pop(0)
	
	
	def Draw(self, givenX, givenY):
		"""
			Draws the chat box and its contents.
		"""
		#Draw(self, givenX, givenY)
		
		y=givenY
		
		for line in self.lines:
			
			self.font.Print(givenX,y,line)
			y+= 10
			
		self.slots['text input'].Draw(givenX, givenY)
		
		
	def Update(self):

		self.Pump()

		
	#receives messages from the server
	def Network_Chat(self, message):
		"""
			Data: message
			
			Adds the received message to the text box.
		"""
		self.AddLine(message['text'])
		
	def SendText(self):
		connection.Send({'action':'Chat', 'text': self.slots['text input'].GetText()})
		self.slots['text input'].Clear()