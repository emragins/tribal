import ika
from data import data
import subwindow

class Button(subwindow.Slot):
	def __init__(self, xOffset, yOffset, text = '', onEnter = None):
		self.font = data.fonts["system"]
		self.margin = 5
		
		self.xOffset = xOffset
		self.yOffset = yOffset
		
		self.text = text
		
		self.width = self.font.StringWidth(self.text) + 2*self.margin
		self.height = self.font.height + 2*self.margin
			
		subwindow.Slot.__init__(self, self.xOffset, self.yOffset, self.width, self.height)
		
		self.color = data.colors['blue']
		
		self.onEnter = onEnter
		
		self.selected = False
		self.selectedColor = data.colors['white']
		
	def Update(self):
		pass
		
	def Draw(self, givenX, givenY):
		x = givenX + self.xOffset
		y = givenY + self.yOffset
		ika.Video.DrawRect(x, y, x + self.width, y + self.height, self.color, 1)
		
		if self.selected:
			ika.Video.DrawRect(x, y, x + self.width, y + self.height, self.selectedColor, 0)
		
		self.font.Print(x + self.margin, y + self.margin, self.text)
	
	def AttachFunction(self, function):
		self.onEnter = function
	
	def ReceivedLeftClick(self, x, y):
		self.OnEnter()
		
	def OnEnter(self):
		try:
			self.onEnter()
		except:
			print 'in button', self.text,'action', self.onEnter, 'failed'
	