import box

"""
looks to me like this is just like box class...
"""

class Slot(box.Box):
	def __init__(self, xOffset, yOffset, width, height, contents = []):
		self.xOffset = xOffset
		self.yOffset = yOffset
		self.width = width
		self.height = height
		
		self.contents = contents
		
		box.Box.__init__(self, self.xOffset, self.yOffset, self.width, self.height)
		
	def Draw(self, givenX, givenY):
		pass
		
	def Update(self):
		pass