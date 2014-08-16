class Box:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		
	def HasPoint(self, x, y):
		print '*checking point', x, y, 'against', self.x, self.width, self.y, self.height
		
		if y >= self.y	\
			and y < self.y + self.height	\
			and x < self.x + self.width	\
			and x >= self.x:
			return True
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
		
		