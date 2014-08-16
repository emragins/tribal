import manager
from mouse import mouse

"""
Controls all the windows on screen
This is what is ran by the rest of the program

WindowManager maintians two lists of windows.  
-One is used simply for searching and the like and is all encampasing. (self.dict as defined by the Manager class)
-The other is a list of layers which is used, well, for keeping the layers in order.  This is 
necessary for drawing and overlapping functionality.  This is also what decides which window gets 
a mouse click when they overlap.

As far as the mouse goes, WindowManager also monitors mouse clicks will dissiminate(sp) 
appropriately with functions:
 
 -Received___Click(x,y)
 -Received___Hold(x,y)
 -Received___Release(x,y)
 
 where each x,y are the current mouse coordinates.
"""

"""
TODO:

There is no support for middle and right mouse buttons.

Maybe clean up code a bit since I think there's various repeated lines that could be turned 
into functions for easier readability.
"""

class WindowManager(manager.Manager):
	def __init__(self):
		manager.Manager.__init__(self)
		self.layers = [{},{},{},{},{}]
		
		self.maxLayer = len(self.layers)
		
	def Update(self):
		
		#--mouse stuff-----------------------------------------
		x = mouse.x
		y = mouse.y
		
		if mouse.LeftClick():
			mouse.LeftClickUsed()
			self.currentWindow = self.EstablishWindow(x,y)
			if self.currentWindow is None:
				pass
			else:
				self.currentWindow.ReceivedLeftClick(x,y)
				
		if mouse.LeftHeld():
			if self.currentWindow is None:
				pass
			else:
				self.currentWindow.ReceivedLeftHold(x,y)
				
		if mouse.LeftReleased():
			mouse.LeftReleaseUsed()
			if self.currentWindow is None:
				pass
			else:
				self.currentWindow.ReceivedLeftRelease(x,y)
		
		#--window stuff----------------------------------------
		#update windows as normal
		for key, obj in self.dict.iteritems():
			obj.Update()
			
		#check if any died
		for key, obj in self.dict.items():	
			if hasattr(obj, "dead") and obj.dead:
				layer = obj.layer
				del self.layers[layer][key]
				del self.dict[key]	
		
		#play with layers if necessary
		for key, obj1 in self.dict.items():	
			if obj1.bringToTop:		##should probably switch to 'hasattr' but want to 
									##know if it breaks/is missing
				#adjust moved object
				if obj1.layer != 0:
					del self.layers[obj1.layer][obj1.id]
					obj1.layer = 0	#set on top
					self.layers[0][obj1.id] = obj1
				
				#check other boxes
				for key, obj2 in self.dict.items():	
					if obj1 != obj2 and	obj1.CollidesWithBox(obj2):
						del self.layers[obj2.layer][obj2.id]
						obj2.layer += 1
						if obj2.layer >= self.maxLayer:
							obj2.layer -= 1
						self.layers[obj2.layer][obj2.id] = obj2
				
				obj1.bringToTop = False		
				break
				
	
	
	def Draw(self):
		for layer in reversed(self.layers):
			for key, obj in layer.items():
				obj.Draw()
	
		
	def Add(self, key, obj):
		self.dict[key] = obj		
		self.layers[0][key] = obj	#assumes that a new window will want to be on top
									
		#play with layers if necessary (ie, window open ontop another
		##untested
		for key, obj2 in self.dict.items():	
			if obj != obj2 and obj.CollidesWithBox(obj2):
				del self.layers[obj2.layer][obj2.id]
				obj2.layer += 1
				if obj2.layer >= self.maxLayer:
					obj2.layer -= 1
				self.layers[obj2.layer][obj2.id] = obj2
	
	#determine which window should receive the mouse action
	def EstablishWindow(self, x, y):
		for layer in self.layers:
			for key, win in layer.items():
				if win.HasPoint(x, y):
					return win
		return None
	
	
windowManager = WindowManager()