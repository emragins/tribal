import manager
from PodSixNet.Connection import ConnectionListener, connection
from mapdata import mapData
import entity
 
class MapEngine(ConnectionListener):
	
	def Update(self):
		mapData.entities.Update()
		
		self.Pump()
		
	def Draw(self):
		mapData.entities.Draw()
		
	def Network_AddEntity(self, data):
		#id,name,x,y
		
		print "Add entity received"
		
		e = entity.Entity(data['id'], data['name'], data['x']*50,data['y']*50) 
		
		#if the player tag is set, let the client know this entity is the client.
		#if data['player'] == 1:
		#	e.player = 1
		print e.x, e.y
		print str(data)
		
		mapData.entities.Add(data['id'], e)
		
	def Network_SetPlayer(self, message):
		#id
		
		print "Set player received"
		
		print message['id']
		
		if mapData.entities.Has(message['id']):
			print "set"
			mapData.entities.Get(message['id']).player = 1
		
	def Network_RemoveEntity(self, data):
		
		del self.entities[data['id']]
		

mapEngine = MapEngine()