import manager
from PodSixNet.Connection import ConnectionListener, connection
from mapdata import mapData
import entity

class MapEngine(ConnectionListener):
	
	def update(self):
		mapData.entities.update()
		
	def draw(self):
		mapData.entities.draw()
		
	def Network_addEntity(self, data):
		#id,x,y,player
		
		e = entity.Entity(data['id'], data['x'],data['y'],self) 
		
		#if the player tag is set, let the client know this entity is the client.
		if data['player'] == 1:
			e.player = 1
		
		mapData.entities.add(data['id'], e)
		
	def Network_removeEntity(self, data):
		
		del self.entities[data['id']]
		

mapEngine = MapEngine()