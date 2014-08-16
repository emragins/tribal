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
		
		self.objectList = manager.Manager()

	def mainLoop(self):
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
		
	def AddObject(self, key, obj):
		
		self.objectList.Add(key, obj)

	def Draw(self):
		
		self.objectList.Draw()

	def Update(self):
		
		self.objectList.Update()
			
engine = GameEngine()