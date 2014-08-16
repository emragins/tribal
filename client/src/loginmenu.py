import ika
from data import data
import window
import text
import button

"""
TODO:

-contents probably a little *TOO* hardcoded
-size hardcoded
"""

"""
total height = 
total width = 
button height = 
button width = 


_________________
|				|
|Name:_________	|
|Pass:_________	|
|				|
|----[SEND]----	|
|_______________|
"""


class LoginMenu(window.Subwindow):
	def __init__(self, x, y):
		self.width = 150
		self.height = 50
		self.margin = 5
		self.wordwidth = 15
		
		self.slots = {}
		self.slots['name input'] = text.InputBox(self.margin + self.wordwidth, self.margin)
		self.slots['password input'] = text.InputBox(self.margin + self.wordwidth, self.margin + 15)
		self.slots['send button'] = button.Button(50, 40, text = "Login")
		
		window.Subwindow.__init__(self, x, y, self.width, self.height, 'login menu', movable = False)
		
		self.backgroundColor = data.colors['green']
		
	def Update(self):
		pass
		
		
	def Draw(self, givenX, givenY):
		ika.Video.DrawRect(givenX, givenY, givenX + self.width, givenY + self.height, self.backgroundColor, 1)
		for key, slot in self.slots.items():
			slot.Draw(givenX, givenY)
			
	def ReceivedLeftClick(self, x, y):
		slot = self.EstablishSlot(x,y)
		#in the event there were None
		try:
			self.slots[slot].ReceivedLeftClick(x,y)
		except:
			pass
		
	def EstablishSlot(self, x, y):
		#establish which slot corrosponds
		print self.slots
		for key, slot in self.slots.items():
			if slot.HasPoint(x, y):
				return key