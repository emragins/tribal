import ika
from data import data
import subwindow

class InputBox(subwindow.Slot):
	def __init__(self, xOffset, yOffset, width = 100):
		self.font = data.fonts["system"]
		self.margin = 2
		self.color = data.colors['dark blue']
		
		self.xOffset = xOffset
		self.yOffset = yOffset
		self.width = width + 2*self.margin
		self.height = self.font.height + 2*self.margin 
		
		self.cursor = '|'
		self.oldCursorPosition = 0
		self.cursorPosition = 0
		
		self.buffer = ''
	
		subwindow.Slot.__init__(self, self.xOffset, self.yOffset, self.width, self.height)
		
		
	def Draw(self, givenX, givenY):
		#background stuff
		x = givenX + self.xOffset
		y = givenY + self.yOffset
		ika.Video.DrawRect(x, y, x + self.width, y + self.height, self.color, 1)
					
		self.font.Print(x+self.margin, y+self.margin, self.buffer)
		
		
		"""
			Checks for keyboard input and add it to the buffer.
		"""
		
		kb = ika.Input.keyboard
		
		if kb.WasKeyPressed(): 
			char = kb.GetKey()
			
			char = self.ProcessChar(char)
			
			if char == '\x08': #backspace
				self.buffer = self.buffer[:-1]
			elif char == '\x7f': #delete
				pass
			else:
				self.buffer += char

	def Update(self):
		kb = ika.Input.keyboard
		
		
				
	def ProcessChar(self, char):
		"""
			Processes a single character for enter or shift processing.
		"""
		
		if len(self.buffer) > self.length:
			return	##maybe sound effect error thing
		
				
		kb = ika.Input.keyboard

		
		special = ['~_+{}|:"<>?', "`-=[];',./"]
		
		if char == '\r': #return key
			connection.Send({"action":"Chat", "text":self.buffer})
			self.buffer = ""
			char =  ''
		elif kb['LSHIFT'].Position() or kb['RSHIFT'].Position():
			if char.isalpha():
				char = char.upper()
			elif char.isdigit():
				char = ')!@#$%^&*('[int(char)]
			elif char in special[1]:
				char = special[0][special[1].index(char)]
			
			
		return char 
		
	def ReceivedLeftClick(self, x, y):
		self.buffer += self.cursor
