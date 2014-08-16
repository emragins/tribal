#Physical representation of a player / NPC
import gametimer
from maplist import MapList
import messages
from direction import direction

class Entity:
	
	def __init__(self,name,id,x,y):
		
		self.x = x
		self.y = y
		
		self.name = name #names are the human-readable identifier of entities.
		self.id = id #ids are the UNIQUE identifier of entities. for players, they are the name preceded by e.
		self.maps = MapList(self)
		
		self.channel = None

		#Client side 60 updates are called per second.
		#Clients move at 1 pixel per update
		#So a client would have its walk animation done 
		#in a little under a second.
		self.moveTimer = gametimer.Timer(.2)
	
	def SetMap(self, map):
		##all of this is kind of wrong
		self.maps.SetCenter(map)
		map.Subscribe(self)
	
	def Move(self, dir):
		
		##Add collision detection.
		
		#print dir
		#print direction["up"].number
		
		if self.moveTimer.IsDone(): #If the client isn't currently moving.
			#print 'move ok'
			self.moveTimer.Reset() #Reset the timer since they're moving again
			
			#Process the direction and just update our position right away
			if dir == direction["up"].number:
				#print 'up'
				self.y -= 1
			elif dir == direction["down"].number:
				#print 'down'
				self.y += 1
			elif dir == direction["left"].number:
				#print 'left'
				self.x -= 1
			elif dir == direction["right"].number:
				#print 'right'
				self.x += 1
				
			#print str(self.x), str(self.y)
				
			msg = messages.Move(self.id, dir)
				
			self.maps.BroadcastExcept(msg,self.id)
				
			return True #Move was succesful
		else:
			print 'move bad from player', self.name
			return False #Move did not succed, let the calling object handle it.
			
	def NetworkMessage(self, message):
		#If we have a channel connected, send it the message.
		#Network messages are NOT to be used for server processing.
		#They are merely for relaying information to connected clients.
		
		if self.channel != None:
			self.channel.Send(message)