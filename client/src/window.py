from windowmanager import windowManager
from data import data
import ika
import box

"""
TODO:

At present ANY hold/release sent to this window is interpretted as a 'drag'.  This needs to 
change.  (Will be a problem if calling window is not draggable.)

HeaderBar (ie, whole window) should expand if title/id is too long to fit.  That or truncate words.

There is no support for middle and right mouse buttons.

"""

"""		
ABOUT WINDOW

-Window class acts as a frame for various aspects of the game
-Subwindow class is used to initialize window class

-Each Window adds itself to the WindowManager upon creation and 
	dies when child dies or is closed. It is then removed by manager.
-Objects use 'dead' system to tell window as much
-Class provides functionaltiy for:
	- 'click the X' closing
	- moving
	- resizeable? I prefer not... too much crap.
"""

"""
ABOUT SUBWINDOW

Seperate 'Subwindow' class to handles objects who wish to be part of a Window.  
	This 'Subwindow' class is inherited and is thenafter ignored.
	
	The class becoming a part of a window will need to have a function to handle mouse clicks.
"""

"""
THINGS TO NOTE:
- sent value of y is the y below the header. (thus only header needs to adjust (at this point anyway))
	Maybe in future could have the window store offsets for each of its children and send those instead.
	I was going to have it that the header sat above the window but this messed up plans for mouse 
		(everything operated by window must be inside of the window)
- mouse works by:
	-windowManager gets click.
	-windowManager goes through layers of windows to find match (if any)
	-windowManager then tells first found window, you got a click at (x,y)
	-window then goes through its parts to determine which part of itself was clicked
		-ie. it will tell either the main part or the header 'you got a click'
	-it is then up to subpart to narrow down the click even more.

- that said, EVERYTHING that a window holds must have stuff for handling mouse clicks.
	I recommend a list of boxes to check, and when box found, then end result happens.
"""



class Window(box.Box):
	def __init__(self, x, y, width, height, id, movable = True):
		#not constant
		self.x = x
		self.y = y
		
		self.movable = movable
		self.contents = []
		
		#constant stuff depended needed by...
		self.width = width
		self.id = id
		
		if self.movable:
			#uses given id and width
			self.header = HeaderBar(self)
			self.Add(self.header)
		
		#depends on everything inside the window.. the main caller is 'height' alone
		#caller DOES NOT get added until after this has passed... contents will not include it
		self.height = height
		for obj in self.contents:
			height += obj.height
		
		#variables specific to controlling the window
		#--dragging---
		self.beingDragged = False
		#initial distance from mouse to corner of window
		self.mouseOffsetX = 0	
		self.mouseOffsetY = 0
		#previous mouse coordinate/position of window
		self.startingX = x	
		self.startingY = y	
		#for counting how often should check for window collisions
		self.dragCounter = 0
		self.bringToTop = False	#becomes true when moved. windowManager sets to False again
		
		self.layer = 0 			#used to determine level of window vs. other windows.
								#	when non-zero, window is/was burried
								
		#other
		self.dead = False
		

		#inheritance stuff
		windowManager.Add(self.id, self)
		box.Box.__init__(self, self.x, self.y, self.width, self.height)
		
		
	def Update(self):
		#check if child(ren) died
		for content in self.contents:
			if hasattr(content, "dead") and content.dead == True:
				self.Die()
			content.Update()
			
	def Draw(self):
		if self.movable:
			y = self.y + self.header.height
		else:
			y = self.y
		for content in self.contents:
			content.Draw(self.x, y)
			
	
	#--For Dragging-------------------------------
	def ReceivedLeftClick(self, x, y):
		xOffset = x - self.x
		yOffset = y - self.y
		for box in self.contents:
			if box.HasPoint(xOffset,yOffset):
				box.ReceivedLeftClick(xOffset,yOffset)
		print self.id, "at point", xOffset, yOffset	###
	
	def ReceivedLeftHold(self, x,y):
		if self.beingDragged:
			self.Drag(x,y)

	def ReceivedLeftRelease(self, x, y):
		if self.beingDragged:
			self.Drag(x,y)
			self.beingDragged = False
			
	def BeginDrag(self, x, y):
		self.mouseOffsetX = x
		self.mouseOffsetY = y
		self.beingDragged = True
		self.startingX = self.x
		self.startingY = self.y
	
	def Drag(self, x, y):
		#only check window layers every so often.. no need to EVERY update
		self.dragCounter += 1
		if self.dragCounter == 10:
			self.bringToTop = True
			self.dragCounter = 0
		
		difX = x - self.startingX
		difY = y - self.startingY
		
		self.x += difX - self.mouseOffsetX
		self.y += difY - self.mouseOffsetY
		
		self.startingX = self.x
		self.startingY = self.y
	#------------------------------------
	
	def Add(self, obj):
		self.contents.append(obj)
	
	def Die(self):
		self.dead = True
		

		
class Subwindow(box.Box):
	def __init__(self, x, y, width, height, id, movable = True):
		self.dead = False
		
		self.xOffset = 0
		self.yOffset = 0
		
		box.Box.__init__(self, 0, 0 + 15, width, height)	##all of this needs to change
															##it's like this because I'm lazy
		
		self.parentWindow = Window(x, y, width, height, id, movable)
		self.parentWindow.Add(self)
	
		
	def Die(self):
		self.dead = True
		
#Bar sits inside window x/y
class HeaderBar(box.Box):
	def __init__(self, parent):
		#offsets not accounted for at present in drawing.
		self.xOffset = 0
		self.yOffset = 0
		
		self.width = parent.width
		self.height = 15
		self.closeBoxWidth = 10
		self.title = parent.id
		
		self.dead = False
		
		self.parent = parent
		
		self.font = data.fonts['system']
		self.mainColor = data.colors['light grey']
		self.closeColor = data.colors['red']
		
		box.Box.__init__(self, self.xOffset, self.yOffset, self.width, self.height)
		
		self.closeBoxOffset = self.width - self.closeBoxWidth
		
		
		#header contents
		self.subboxes = {}
		self.subboxes['main'] = box.Box(self.xOffset, self.yOffset, self.closeBoxOffset, self.height)
		self.subboxes['close'] = box.Box(self.xOffset + self.closeBoxOffset, self.yOffset, self.closeBoxWidth, self.height)
		
	def Draw(self, givenX, givenY):
		#main bar
		ika.Video.DrawRect(givenX, givenY - self.height, givenX + self.closeBoxOffset, givenY, self.mainColor, 1) 
		#closing rectangle
		ika.Video.DrawRect(givenX + self.closeBoxOffset, givenY- self.height, givenX + self.width, givenY + self.height, self.closeColor, 1)
		
		#title
		self.font.Print(givenX, givenY - self.height, self.title)
		
	#receives offset x, y from 0,0
	def ReceivedLeftClick(self, x, y):
		print 'subboxes in header', self.subboxes	###
		for key, box in self.subboxes.items():
			print 'box', box	##
			if box.HasPoint(x,y):
				
				if key is 'close':
					print 'header dies'###
					self.Die()
				elif key is 'main':
					print 'begin drag'###
					self.parent.BeginDrag(x,y)
		
	
	def Update(self):
		pass
	def Die(self):
		self.dead = True