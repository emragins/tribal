import fps
import ika
import manager
from data import data

class GameEngine:
	
	def __init__(self):
		
		self.fpsManager = fps.FPSManager(60)
		ika.SetCaption("TRIBAL")
		
		self.lastUpdate = 0
		self.lastFPS = 0
		
		self.currentFrame = 0
		
		self.objectList0 = manager.Manager()
		self.objectList1 = manager.Manager()
		self.objectList2 = manager.Manager()
		
		self.objectLists = [self.objectList0, self.objectList1, self.objectList2]
		
	def MainLoop(self):
		while 1:

			if ika.GetTime() >= self.lastUpdate:
				
				self.lastUpdate= ika.GetTime()            

				if self.lastFPS != ika.GetFrameRate():
					
					self.lastFPS = ika.GetFrameRate()
					#ika.SetCaption(str(self.LastFPS))
				
				ika.Input.Update()
				
				self.Update()
				
				self.currentFrame += 1
				if self.currentFrame > 60:
					self.currentFrame = 0
				
				self.lastUpdate = ika.GetTime()+1
			
			#print "%s - %s" %(ika.GetTime(), self.CurrentFrame)
				
			self.fpsManager.render(self.Draw)	
		
	def AddObject(self, key, obj, priority):
		
		self.objectLists[priority].Add(key, obj)

	def Draw(self):
		
		for list in reversed(self.objectLists):
			list.Draw()

	def Update(self):
		if len(data.kbControlList) != 0:
			data.kbControlList[len(data.kbControlList) - 1].UpdateKeyboard()
			
		##probably doesn't need to be reversed--oh well
		for list in reversed(self.objectLists):
			list.Update()
			
engine = GameEngine()