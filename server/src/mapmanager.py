
import map

class MapManager:
	
	WORLD_WIDTH = 50 #In terms of maps
	WORLD_HEIGHT = 50
	
	def __init__(self):
		
		self.maps = [] 
		
		#Creates a 2 dimensional array of maps.
		for x in range(self.WORLD_WIDTH):
			ylist = [ ]
			for y in range(self.WORLD_HEIGHT):
				ylist.append(map.Map(x,y))
				
			self.maps.append(ylist)
			
mapManager = MapManager()