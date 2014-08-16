"""
These classes are exactly the same except one uses pure x/y and one uses offset.
The distinction is necessary because it enables these classes to track changes in their
parents.

Frame is for big windows--actual x/y coords.
Box is for pretty much everything else--relative x/y coords.
"""

class Frame:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		
	def HasPoint(self, x, y):
		print 'testing has point', x, y, 'in', self.x, self.width, self.y, self.height
		if y >= self.y	\
			and y < self.y + self.height	\
			and x < self.x + self.width	\
			and x >= self.x:
			print 'true'
			return True
		print 'false'
		return False
		
	def CollidesWithBox(self, box):
		#check four corners of box... if a corner overlaps, then collides
		#probably more efficient way, but feeling kinda lazy
		if self.HasPoint(box.x, box.y):
			return True
		if self.HasPoint(box.x, box.y + box.height):
			return True
		if self.HasPoint(box.x + box.width, box.y):
			return True
		if self.HasPoint(box.x + box.width, box.y + box.height):
			return True
			
		return False
		
	def ChangeWidth(self, w):
		self.width = w
		
		
class Box:
	def __init__(self, xOffset, yOffset, width, height):
		self.xOffset = xOffset
		self.yOffset = yOffset
		self.width = width
		self.height = height
		self.selected = False
		
	def HasPoint(self, x, y):
		print 'testing has point', x, y, 'in', self.xOffset, self.width, self.yOffset, self.height
		if y >= self.yOffset	\
			and y < self.yOffset + self.height	\
			and x < self.xOffset + self.width	\
			and x >= self.xOffset:
			print 'true'
			return True
		print 'false'
		return False
		
	def CollidesWithBox(self, box):
		#check four corners of box... if a corner overlaps, then collides
		#probably more efficient way, but feeling kinda lazy
		if self.HasPoint(box.xOffset, box.yOffset):
			return True
		if self.HasPoint(box.xOffset, box.yOffset + box.height):
			return True
		if self.HasPoint(box.xOffset + box.width, box.yOffset):
			return True
		if self.HasPoint(box.xOffset + box.width, box.yOffset + box.height):
			return True
			
		return False
		
	
	def LostFocus(self):
		self.DeSelect()
		
	def DeSelect(self):
		self.selected = False
	def Select(self):
		self.selected = True	
	def IsSelected(self):
		return self.selected