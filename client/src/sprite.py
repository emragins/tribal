from data import data
from direction import direction

class Sprite:
	
	"""
		Sprites are the visual representation of game entities
	"""
	
	def __init__(self, image):
		
		self.images = data.spriteImages[image]
		
		self.layer = 0
		
		self.direction = direction["up"]
		self.frame = 0
		
		
	def draw(self, x, y):
		
		self.images[self.frame].Blit(x, y)
		