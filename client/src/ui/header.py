from data import data
import ika
import subwindow


class Header(subwindow.Subwindow):
	def __init__(self, parent):
		
		self.font = data.fonts['system']
		self.mainColor = data.colors['light grey']
		self.closeColor = data.colors['red']
		self.minimizeColor = data.colors['orange']
		
		#header naturally goes top left of a window
		self.id = 'header'
		
		self.text = str(parent.id)
		
		self.height = 15

		self.miniBoxWidth = 15
		self.width = self.font.StringWidth(self.text) + 2*self.miniBoxWidth
		self.closeBoxOffset = self.width - self.miniBoxWidth
		self.minimizeBoxOffset = self.closeBoxOffset - self.miniBoxWidth
		
		subwindow.Subwindow.__init__(self, self.width, self.height, self.id)
				
		self.parent = parent
	
		#header contents--defines mouse regions only
		self.slots['main'] = subwindow.Slot(self.xOffset, self.yOffset, self.closeBoxOffset, self.height)
		self.slots['minimize'] = subwindow.Slot(self.xOffset + self.minimizeBoxOffset, self.yOffset, self.miniBoxWidth, self.height)
		self.slots['close'] = subwindow.Slot(self.xOffset + self.closeBoxOffset, self.yOffset, self.miniBoxWidth, self.height)
		
	def Draw(self, givenX, givenY):
		#main bar
		ika.Video.DrawRect(givenX, givenY, givenX + self.minimizeBoxOffset, givenY + self.height, self.mainColor, 1) 
		#minimize rectangle
		ika.Video.DrawRect(givenX + self.minimizeBoxOffset, givenY, givenX + self.closeBoxOffset, givenY + self.height, self.minimizeColor, 1)
		#closing rectangle
		ika.Video.DrawRect(givenX + self.closeBoxOffset, givenY, givenX + self.width, givenY + self.height, self.closeColor, 1)
		
		#title
		self.font.Print(givenX, givenY, self.text)
		
	#receives offset x, y from 0,0
	def ReceivedLeftClick(self, x, y):
		for key, box in self.slots.items():
			if box.HasPoint(x,y):
				
				if key is 'close':
					self.Die()
				elif key is 'minimize':
					self.parent.Minimize()
				elif key is 'main':
					self.parent.BeginDrag(x,y)
		
	
	def Update(self):
		pass
	def Die(self):
		self.dead = True
		
	def UpdateWidth(self, w):
		self.width = w
		self.closeBoxOffset = self.width - self.miniBoxWidth
		self.minimizeBoxOffset = self.closeBoxOffset - self.miniBoxWidth
		
		##should be better way.. it won't/can't automatically update in box
		##because not initialized with "width", but ___& miniBoxOffset
		self.slots['main'].width = self.minimizeBoxOffset
		self.slots['minimize'].xOffset = self.xOffset + self.minimizeBoxOffset
		self.slots['close'].xOffset = self.xOffset + self.closeBoxOffset