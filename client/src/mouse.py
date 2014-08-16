import ika

"""
Work in progress.
"""

pointers = {
			"default": ika.Image("images\\default pointer.png")
			}

##should be better way
import manager
class MouseManager:
	def __init__:
		mice = manager.Manager()
		
	def Add(self, obj):
		
		manager.

			
class Mouse:
	def __init__(self, type = 'default'):
		##should probably initialize these to something else
		self.x = 300
		self.y = 300
		self.type = type
		
		global pointers
		self.pointer = pointers[self.type]
		
		self.position = 'up'
		self.positions = {'down': 1,
						'up': 0
						}
				
		
	def Draw(self):
		self.pointer.Blit(self.x, self.y, 1)
		
	def Update(self):
		mouse = ika.Input.mouse
		
		self.x = mouse.x
		self.y = mouse.y
		
		if mouse.left.Pressed():
			print 'clicked left button at', self.x, self.y
		if mouse.right.Pressed():
			print 'clicked right button at', self.x, self.y
		if mouse.middle.Pressed():
			print 'clicked middle button at', self.x, self.y
			
		
		if mouse.left.Position():
			print 'held left button at', self.x, self.y
		if mouse.right.Position():
			print 'held right button at', self.x, self.y
		if mouse.middle.Position():
			print 'held middle button at', self.x, self.y
	
	def GetStatus(self):
		return self.position
	
	def GetXY(self):
		return self.x, self.y
		
mouse = Mouse()