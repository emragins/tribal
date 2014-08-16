import messages

class Map:
	
	def __init__(self, x, y):
		
		self.x = x
		self.y = y
		
		self.entities = [] #entities that are on this map.
		
	def Subscribe(self, entity):	
		
		##need a more automated way to do this	

		if entity not in self.entities:
			self.entities.append(entity)
		
		for e in self.entities:
			entity.NetworkMessage( messages.AddEntity(e.id,e.name,e.x,e.y) ) #tell new entity what's on the map.
			if e is not entity:
				e.NetworkMessage( messages.AddEntity(entity.id, entity.name, entity.x, entity.y) ) #tell old entities about new entity.
			
		entity.NetworkMessage( messages.SetPlayer(entity.id) )
		
	def Update(self):
		#Calls the required updates on its list of entities.
		pass
		
	def Broadcast(self, message):
		#Sends a message to all of its entities.
		#If an entity doesn't have a channel it will ignore the broadcast.
		
		for e in self.entities:
			e.NetworkMessage(message)
			
	def BroadcastExcept(self, message, id):
		#Sends a message to all of its entities.
		#If an entity doesn't have a channel it will ignore the broadcast.
		
		for e in self.entities:
			if e.id != id:
				e.NetworkMessage(message)