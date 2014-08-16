import ika
from PodSixNet.Connection import ConnectionListener, connection
from data import data
import window, subwindow
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


class LoginMenu(ConnectionListener, subwindow.Subwindow):
	def __init__(self, x, y):
		self.width = 150
		self.height = 70
		self.margin = 5
		self.wordwidth = 15
		self.id = 'login menu'
		
		subwindow.Subwindow.__init__(self, self.width, self.height, self.id)
		
		self.slots['name input'] = text.InputBox(self.margin + self.wordwidth, self.margin)
		self.slots['password input'] = text.InputBox(self.margin + self.wordwidth, self.margin + 15)
		self.slots['send button'] = button.Button(50, 40, text = "Login", onEnter = self.VerifyData)
		self.slots['password input'].HideText()
		
		self.tabCycle.append(self.slots['name input'])
		self.tabCycle.append(self.slots['password input'])
		self.tabCycle.append(self.slots['send button'])
		
		window.NewWindow(self, x, y, self.width, self.height, self.id, movable = False)
		
		self.backgroundColor = data.colors['green']
		
	def VerifyData(self):
		name = self.slots['name input'].GetText()
		password = self.slots['password input'].GetText()
		
		connection.Send({'action':'Login', 'name': name, 'password': password})
		
		self.Die()
		##!!INPUT CODE TO CHECK DATA!!
	