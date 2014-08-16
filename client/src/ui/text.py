import ika
from data import data
import subwindow
from mouse import mouse

class InputBox(subwindow.Slot):
	def __init__(self, xOffset, yOffset, width = 100, onEnter = None):
		self.font = data.fonts["system"]
		self.margin = 2
		self.color = data.colors['blue']
		self.selectedColor = data.colors['red']
		
		self.xOffset = xOffset
		self.yOffset = yOffset
		
		self.cursor = '_' 	# '|' does not work with current font
		
		self.oldCursorPosition = 0
		self.cursorPosition = 0
		
		cursorWidth = self.font.StringWidth(self.cursor)	
		self.width = width + 2*self.margin 
		self.length = int((self.width - cursorWidth)/self.font.width) 	#need room for cursor on line
		self.height = self.font.height + 2*self.margin 
		
		
		self.buffer = ''
		self.hideText = False
		
		self.selected = False
		self.onEnter = onEnter
		
		subwindow.Slot.__init__(self, self.xOffset, self.yOffset, self.width, self.height)
		
	def Draw(self, givenX, givenY):
		#background stuff
		x = givenX + self.xOffset
		y = givenY + self.yOffset
		string = ''
		if self.hideText:
			for i in range(len(self.buffer)):
				string += '*'
			if self.selected:
				ika.Video.DrawRect(x, y, x + self.width, y + self.height, self.selectedColor, 1)
				string = string[:self.cursorPosition] + self.cursor + string[self.cursorPosition:]
			else:	
				ika.Video.DrawRect(x, y, x + self.width, y + self.height, self.color, 1)
		else:
			if self.selected:
				ika.Video.DrawRect(x, y, x + self.width, y + self.height, self.selectedColor, 1)
				string = self.buffer[:self.cursorPosition] + self.cursor + self.buffer[self.cursorPosition:]
			else:
				ika.Video.DrawRect(x, y, x + self.width, y + self.height, self.color, 1)
				string = self.buffer
			
		
		
				
		self.font.Print(x+self.margin, y+self.margin, string)
		
	def UpdateKeyboard(self):
		
		"""
			Checks for keyboard input and add it to the buffer.
		"""
		
		kb = ika.Input.keyboard
		
		if kb['LEFT'].Pressed():
			if self.cursorPosition > 0:
				self.cursorPosition -=1
		elif kb['RIGHT'].Pressed():
			if self.cursorPosition < len(self.buffer):
				self.cursorPosition +=1
		'''	
		if kb.Position():
			if self.leftPressed is False:
				print 'left click'
				self.leftClicked = True
				self.timer.Reset()
				self.doubleTimer.Reset()
				self.leftPressed = True
			elif self.leftPressed and self.timer.IsDone():
				self.leftHeld = True
		'''
		if kb.WasKeyPressed(): 
			char = kb.GetKey()
			
			char = self.ProcessChar(char)
			
			if char == '\x08': #backspace
				if self.cursorPosition == len(self.buffer):
					try:
						self.buffer = self.buffer[:-1]
						self.cursorPosition -= 1
					except:
						pass
				elif self.cursorPosition == 0:
					pass
				else:
					#try:
					self.buffer = self.buffer[:self.cursorPosition-1]+ self.buffer[self.cursorPosition:]
					self.cursorPosition -= 1
					#except:
					#	pass
			elif char == '\x7f': #delete
				if self.cursorPosition == 0:
					try:
						self.buffer = self.buffer[1:]
					except:
						pass
				else:
					try:
						self.buffer = self.buffer[:self.cursorPosition]+ self.buffer[self.cursorPosition+1:]
					except:
						pass
			elif char == '\x09': #tab
				pass
			else:
				#need try because when run out of room, returns 'nonetype' character
				try:
					
					self.buffer = self.buffer[:self.cursorPosition] + char + self.buffer[self.cursorPosition:]
					self.cursorPosition += 1
				except:
					pass
	
	def ProcessChar(self, char):
		"""
			Processes a single character for enter or shift processing.
		"""
		
		
		if len(self.buffer) > self.length:	
			return	##maybe sound effect error thing
		
				
		kb = ika.Input.keyboard

		
		special = ['~_+{}|:"<>?', "`-=[];',./"]
		
		if char == '\r': #return key
			self.OnEnter()
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
		if self.selected:
			pass
		else:
			self.Select()
		
	def GetText(self):
		return self.buffer
	
		
	def OnEnter(self):
		try:
			self.onEnter()
		except:
			print 'in textfield', self,'action', self.onEnter, 'failed'
	
	def Clear(self):
		self.buffer = ''
		self.oldCursorPosition = 0
		self.cursorPosition = 0
	
	def HideText(self):
		self.hideText = True
	def UnhideText(self):
		seld.hideText = False