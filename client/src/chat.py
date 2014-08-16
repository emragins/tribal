import ika
from PodSixNet.Connection import ConnectionListener, connection
from data import data


class ChatBox(ConnectionListener): 
	
	def __init__(self):
		
		self.font = data.fonts["system"]
		
		self.lines = [] #currently displayed lines
		self.buffer = '' #the text that the user is currently typing.
		self.maxLines = 10 #number of lines that can be displayed at any one time.
		
	
	def addLine(self, text):
		"""
			Adds a single line of text to the chat box
		"""
		
		self.lines.append(text)
		
		if len(self.lines) > self.maxLines:
			self.lines.pop(0)

	def draw(self):
		"""
			Draws the chat box and its contents.
		"""
		
		y=0
		
		for line in self.lines:
			
			self.font.Print(0,y,line)
			y+= 10
			
					
		self.font.Print(0,590, ">"+self.buffer)

	def processChar(self, char):
		"""
			Processes a single character for enter or shift processing.
		"""
		
		kb = ika.Input.keyboard
		
		special = ['~_+{}|:"<>?', "`-=[];',./"]
		
		if char == '\r': #return key
			connection.Send({"action":"message", "message":self.buffer})
			self.buffer = ''
		elif kb['LSHIFT'].Position() or kb['RSHIFT'].Position():
			if char.isalpha():
				char = char.upper()
			elif char.isdigit():
				char = ')!@#$%^&*('[int(char)]
			elif char in special[1]:
				char = special[0][special[1].index(char)]
				
		return char 
		
	def update(self):
		"""
			Checks for keyboard input and add it to the buffer.
		"""
		
		kb = ika.Input.keyboard
		
		if kb.WasKeyPressed(): 
			char = kb.GetKey()
			
			char = self.processChar(char)
			
			if char == '\x08': #backspace
				self.buffer = self.buffer[:-1]
			elif char == '\x7f': #delete
				pass
			else:
				self.buffer += char
				
		self.Pump()
		
	#receives messages from the server
	def Network_message(self, data):
		"""
			Data: message
			
			Adds the received message to the text box.
		"""

		self.addLine(data['message'])