from windowmanager import windowManager
import box
import subwindow
import header
from data import data
import ika
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

class NewWindow:
	def __init__(self, callingWindow, x, y, width, height, id, movable = True):
		
		window = Window(x, y, id, movable = True)
		
		if movable:
			#uses given id and width
			head = header.Header(window)
			window.Add('header', head)
			callingWindow.yOffset += head.height
		
		window.Add(id, callingWindow)
		
		
		
class Window(box.Frame):
	def __init__(self, x, y, id, movable = True):
		#not constant
		self.x = x
		self.y = y
		self.height = 0
		self.expandedHeight = self.height
		self.width = 0
		
		box.Frame.__init__(self, self.x, self.y, self.width, self.height)
		
		self.movable = movable
		self.contents = {}
		
		
		#constant stuff depended needed by...
		self.id = id
				
		
		
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
		self.minimized = False
		self.dead = False
		

		#inheritance stuff
		windowManager.Add(self.id, self)
		#self
		
	def Update(self):
		#check if child(ren) died
		for key, content in self.contents.items():
			if hasattr(content, "dead") and content.dead == True:
				self.Die()
			if content.hidden is False:
				content.Update()
			
	def Draw(self):
	
		if self.minimized:
			#border
			##color
			ika.Video.DrawRect(self.x-1, self.y-1, self.x + self.width + 1, self.y + self.contents['header'].height + 1, data.colors['white'], 0)
			self.contents['header'].Draw(self.x + 0, self.y +0)	##sloppy
		
		else:
			#border
			##color
			ika.Video.DrawRect(self.x-1, self.y-1, self.x + self.width + 1, self.y + self.height + 1, data.colors['white'], 0)
			#internal box
			##color
			ika.Video.DrawRect(self.x, self.y, self.x + self.width, self.y + self.height, data.colors['dark blue'], 1)
				
			for key, content in self.contents.items():
				content.Draw(self.x + content.xOffset, self.y + content.yOffset)
			
	
	#--For Dragging-------------------------------
	def ReceivedLeftClick(self, x, y):
		mouseXOffset = x - self.x
		mouseYOffset = y - self.y
		
		print 'testing point', mouseXOffset, mouseYOffset
		
		for key, box in self.contents.items():
			print box, box.xOffset, box.width, box.yOffset, box.height
			if box.hidden is False and box.HasPoint(mouseXOffset,mouseYOffset):
				box.ReceivedLeftClick(mouseXOffset,mouseYOffset)
				##break		#belongs but taken out for testing
	
	def ReceivedLeftHold(self, x,y):
		if self.beingDragged:
			self.Drag(x,y)

	def ReceivedLeftRelease(self, x, y):
		if self.beingDragged:
			self.Drag(x,y)
			self.beingDragged = False
	def ReceivedLeftDoubleClick(self, x, y):
		##again, could/should probably just use previously selected subwindow
		mouseXOffset = x - self.x
		mouseYOffset = y - self.y
		
		for key, box in self.contents.items():
			print box, box.xOffset, box.width, box.yOffset, box.height
			if box.hidden is False and box.HasPoint(mouseXOffset,mouseYOffset):
				box.ReceivedLeftDoubleClick(mouseXOffset,mouseYOffset)
				##break		#belongs but taken out for testing
				
	def ReceivedRightClick(self, x, y):
		pass
	def ReceivedRightHold(self, x, y):
		pass
	def ReceivedRightRelease(self,x,y):
		pass
			
	
	def ReceivedMiddleClick(self, x, y):
		pass
	def ReceivedMiddleHold(self, x, y):
		pass
	def ReceivedMiddleRelease(self,x,y):
		pass

	
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
	
	
	
	def Add(self, id, obj):
		self.contents[id] = obj
		self.height += obj.height
		self.expandedHeight = self.height
		
		if obj.width > self.width:
			self.width = obj.width
			
			for key, obj in self.contents.items():
				obj.UpdateWidth(self.width)
			
	def Die(self):
		self.dead = True
		
	def LostFocus(self):
		for key, content in self.contents.items():
			content.LostFocus()	
	
	def Minimize(self):
		if self.minimized:
			self.minimized = False
			self.height = self.expandedHeight
			for key, obj in self.contents.items():
				obj.Unhide()
		else:
			self.minimized = True
			for key, obj in self.contents.items():
				if key is 'header':
					self.height = obj.height
				else:
					obj.Hide()
				