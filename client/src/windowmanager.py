import manager
"""
Very much a work in progress
"""

##Alternative to objects telling parents to delete 'self', use dead/alive system
##	probably a lot cleaner


"""
Controls all the windows on screen
This is what is ran by the rest of the program
"""
class WindowManager(manager.Manager):
	pass
	'''
	def __init__(self):
		self.windows = manager.Manager()
		
	def Add(self, key, obj):
		self.windows.Add(self.nextID, obj)
		self.nextID += 1
	
	def Remove(self, key):
		self.windows.Remove(key)
		
	def Update(self):
		self.windows.Update()
	
	def Draw(self):
		self.windows.Draw()
	'''
	
windowManager = WindowManager()