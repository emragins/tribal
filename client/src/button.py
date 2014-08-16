import ika
from data import data
import subwindow

class Button(subwindow.Slot):
	def __init__(self, xOffset, yOffset, text = '', perform = None):
		self.font = data.fonts["system"]
		self.margin = 5
		
		self.xOffset = xOffset
		self.yOffset = yOffset
		
		self.text = text
		
		self.width = self.font.StringWidth(self.text) + 2*self.margin
		self.height = self.font.height + 2*self.margin
			
		subwindow.Slot.__init__(self, self.xOffset, self.yOffset, self.width, self.height)
		
		self.color = data.colors['blue']
		
		self.perform = perform
		
	def Update(self):
		pass
		
	def Draw(self, givenX, givenY):
		x = givenX + self.xOffset
		y = givenY + self.yOffset
		ika.Video.DrawRect(x, y, x + self.width, y + self.height, self.color, 1)
		
		self.font.Print(x + self.margin, y + self.margin, self.text)
	
	def AttachAction(self, function):
		self.perform = function
	
	def ReceivedLeftClick(self, x, y):
		try:
			self.perform
		except:
			print 'in button action', self.perform, 'failed'
			
		##input code to submit and check data