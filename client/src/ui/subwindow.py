import box
from data import data
import ika

"""
TODO:
change colors on draw to not-hardcoded

Can probably move select/deselct to Box class

----
TABS... should be a better way. 
Presently maintains two lists:
	slots
	tabcycle
And two trackers:
	currentSlot
	tabPosition
	
Because slots is dict, there is no predictable order, hence tabcycle.
Upon a selection, 'tabCycle' is searched for correct 'tabPosition'.
Upon 'tab', 'slots' is searched  for corrosponding key for 'currentSlot'
In this way everything stays aligned, but seems like a lot for so little.
"""

class Slot(box.Box):
	def __init__(self, xOffset, yOffset, width, height, contents = []):
		self.xOffset = xOffset
		self.yOffset = yOffset
		self.width = width
		self.height = height
		
		self.contents = contents
		self.selected = False
		
		box.Box.__init__(self, self.xOffset, self.yOffset, self.width, self.height)
		
	def Draw(self, givenX, givenY):
		pass
		
	def Update(self):
		pass
		
	"""
	These functions are here mainly to prevent existance errors.
	To be used they must be overridden.
	
	Idea:
	Just have leftclick 'select' window and maybe call function.
	"""
	def ReceivedLeftClick(self, x, y):
		self.Select()
	def ReceivedLeftHold(self, x, y):
		pass
	def ReceivedLeftRelease(self,x,y):
		pass
	def ReceivedLeftDoubleClick(self, x, y):
		pass
	
	def ReceivedRightClick(self, x, y):
		pass
	def ReceivedRightHold(self, x, y):
		pass
	def ReceivedRightRelease(self,x,y):
		pass
			
	def ReceivedMiddleClick(self, x, y):
		pass
	def ReceivedMiddleHold(self, x, y):
		pass
	def ReceivedMiddleRelease(self,x,y):
		pass
		
		
		
class Subwindow(box.Box):
	def __init__(self, width, height, id, movable = True):
		self.dead = False
		
		self.xOffset = 0
		self.yOffset = 0
		self.width = width
		self.height = height
		
		self.hidden = False
		
		self.slots = {}
		self.currentSlot = None
		
		self.tabCycle = []
		self.tabPosition = 0
		
		box.Box.__init__(self, self.xOffset, self.yOffset, self.width, self.height)
	
	def UpdateKeyboard(self):
		kb = ika.Input.keyboard
		if kb['TAB'].Pressed():
			self.Tab()
		if kb['RETURN'].Pressed():
			if self.currentSlot != None:
				self.slots[self.currentSlot].OnEnter()
		
		"""
		Note: This will eat ANY errors made in any slots' keyboard update!
		"""
		try:
			self.slots[self.currentSlot].UpdateKeyboard()
		except:
			pass
	
	def Update(self):
		for key, slot in self.slots.items():
			slot.Update()
		
	def Draw(self, givenX, givenY):
		
		for key, slot in self.slots.items():
			slot.Draw(givenX, givenY)
		
		
	
	#coords received are given as if window is at (0,0)
	def ReceivedLeftClick(self, x, y):
		if self.IsSelected() is False:
			self.Select()
			
		mouseXOffset = x - self.xOffset
		mouseYOffset = y - self.yOffset
		
		slot = self.EstablishSlot(mouseXOffset,mouseYOffset)
		if self.currentSlot != slot:
			try:
				self.slots[self.currentSlot].LostFocus()
			except:
				pass
			self.currentSlot = slot
			self.tabPosition = self.EstablishTabPosition(self.currentSlot)
		#in the event there were None
		try:
			self.slots[self.currentSlot].ReceivedLeftClick(x,y)
		except:
			pass
		
	def ReceivedLeftHold(self, x, y):
		pass
	def ReceivedLeftRelease(self,x,y):
		pass
 	def ReceivedLeftDoubleClick(self, x, y):
		##probably DON'T need mouse coordinates here
		mouseXOffset = x - self.xOffset
		mouseYOffset = y - self.yOffset
		
		try:
			self.slots[self.currentSlot].ReceivedLeftDoubleClick(x,y)
		except:
			pass
	def ReceivedRightClick(self, x, y):
		pass
	def ReceivedRightHold(self, x, y):
		pass
	def ReceivedRightRelease(self,x,y):
		pass
			
	
	def ReceivedMiddleClick(self, x, y):
		pass
	def ReceivedMiddleHold(self, x, y):
		pass
	def ReceivedMiddleRelease(self,x,y):
		pass
	
	def EstablishSlot(self, x, y):
		#establish which slot corrosponds
		for key, slot in self.slots.items():
			if slot.HasPoint(x, y):
				return key
	
	def UpdateWidth(self, w):
		self.width = w
	
	def Die(self):
		self.dead = True
	
	def LostFocus(self):
		self.DeSelect()
		for key, slot in self.slots.items():
			slot.LostFocus()
	
	def Hide(self):
		self.LostFocus()
		self.hidden = True
	def Unhide(self):
		self.hidden = False
		
	def Tab(self):
		self.tabPosition += 1
	
		try:
			self.tabCycle[self.tabPosition].Select()
			self.tabCycle[self.tabPosition-1].DeSelect()
		except:
			self.tabPosition = 0
			self.tabCycle[self.tabPosition].Select()
			
			n = len(self.tabCycle)
			self.tabCycle[n-1].DeSelect()
			
		self.currentSlot = self.EstablishSlotKey(self.tabCycle[self.tabPosition])
	
	def EstablishSlotKey(self, obj):
		for key, slot in self.slots.items():
			if slot == obj:
				return key
	def EstablishTabPosition(self, name):
		for i, obj in enumerate(self.tabCycle):
			if obj == self.slots[name]:
				return i
	
	def DeSelect(self):
		if self.selected:
			self.selected = False
			data.kbControlList.remove(self)
	def Select(self):
		data.kbControlList.append(self)
		self.selected = True
		