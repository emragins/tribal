from windowmanager import windowManager
from data import data
import ika
from mouse import mouse

"""
Very much a work in progress
"""

"""		
-Window class acts as a frame for various aspects of the game
-Each Window adds itself to the WindowManager upon creation and 
	dies upon deletion (removed by manager)
-Objects who use the class will add themselves to a Window upon 
	creation
-Objects use 'dead' system to tell window as much
-Class provides functionaltiy for:
	- 'click the X' closing
	- moving
	- resizeable? I prefer not... too much crap.
	
Seperate 'Subwindow' class to handles objects who wish to be part of a Window.  
	This 'Subwindow' class is inherited and is thenafter ignored.
"""

class Window:
	def __init__(self, x, y, width, height, id):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.id = id
		self.dead = False
		self.contents = []
		
		header = HeaderBar(self)
		self.Add(header)
		
		windowManager.Add(self.id, self)
		
	def Update(self):
		"""
		- ( ) - add mouse detection. (probably need whole mouse class)
		- ( ) - add movable windows
		"""
		
		for content in self.contents:
			if hasattr(content, "dead") and content.dead == True:
				self.Die()
			content.Update()
			
	def Draw(self):
		for content in self.contents:
			content.Draw(self.x, self.y)
			
		
	
	def Add(self, obj):
		self.contents.append(obj)
	
	def Die(self):
		self.dead = True
		

		
class Subwindow:
	def __init__(self, x, y, width, height, id):
		self.dead = False
		self.parentWindow = Window(x, y, width, height, id)
		self.parentWindow.Add(self)
	
	def Die(self):
		self.dead = True
		
#Bar sits above the Window's x/y rather than inside it
class HeaderBar:
	def __init__(self, parent):
		self.width = parent.width
		self.height = 15
		self.closeBoxWidth = 10
		self.title = parent.id
		
		self.font = data.fonts['system']
		self.mainColor = data.colors['light grey']
		self.closeColor = data.colors['red']
		
	def Draw(self, givenX, givenY):
		my_y = givenY - self.height
		#main bar
		ika.Video.DrawRect(givenX, my_y, givenX + self.width, givenY, self.mainColor, 1) 
		#closing rectangle
		ika.Video.DrawRect(givenX + self.width - self.closeBoxWidth, my_y, givenX + self.width, givenY, self.closeColor, 1)
		
		#title
		self.font.Print(givenX, givenY - self.height, self.title)
		
	def Update(self):
		pass
	
	def UpdateMouse(self):
		mouseStatus = mouse.GetStatus()
		if mouseStatus is 'up':
			return
		if mouseStatus is 'down':
			x1, y1 = mouse.GetXY()
			
		"""
		add mouse stuff here for:
			-closing
			-moving (will have to figure out rectangle made my mouse coords and adjust
				parent window accordingly)
		"""