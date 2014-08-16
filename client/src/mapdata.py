import manager
from PodSixNet.Connection import ConnectionListener, connection


class MapData:
	
	def __init__(self):
		
		self.tileWidth = 50
		self.tileHeight = 50
		
		self.tileSet = [ ]
		
		self.entities = manager.Manager()
		
mapData = MapData()