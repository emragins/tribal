
class MapList:
	"""
		Stores map references an entity belongs to and handles
		map transitions for it.
	"""
	
	def __init__(self, entity):
		
		self.entity = entity
		
		#Entities subscribe to 9 maps at a time. The map they're on (center) 
		#and the 8 maps surrounding it. They receive and send updates to all 9.
		self.maps = {
				  "L": None, "R": None, "D": None, "U": None,
				  "UL": None, "UR": None, "DL": None, "DR": None,
				  "Center": None
				 }
		
	def SetCenter(self, map):
		##Future editions need to find the surrounding maps as well.
		self.maps["Center"] = map
		
	def Broadcast(self, message):
		
		#for m in self.maps.iteritems():
		#	if m is not None:
		#		m.Broadcast(message)
		
		self.maps["Center"].Broadcast(message)
		
	def BroadcastExcept(self, message, id):
		
		#for m in self.maps.iteritems():
		#	if m is not None:
		#		m.Broadcast(message)
		
		self.maps["Center"].BroadcastExcept(message,id)		
