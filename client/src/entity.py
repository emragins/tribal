"""
	TODO: pretty much rewrite all of this.
	
-The server sends MoveDirection and StopMove commands. 
  These commands include the direction and final/starting x/y.
-When a stop or move command is received, the client calculates a compensation direction queue to correct 
  for the proper x/y. If it's too far away the client says screw it and teleports the entity.
-Otherwise when set to moving the client continually moves the entity in that direction until a stop is received. 
-If there's a queue the calculated moves are added to it while the queue is executed.	
"""

"""
NEW SYSTEM

When moving, the client sends the server the direction it wants and starts moving. It does this for each tile.
If the server notices that it's sent too soon since the last one or into a collision coordinate, it rejects it and
sends the player the x/y/direction it should be at to warp to.

When other players are moving, the client sends the individual move packets to every client. Each client
adds the direction to its queue to move.

When entering a new partition, the server sends the id and x/y/direction of every entity on the map to the player.
It then begins to update them for the client.
The partition left behind has its entities deleted.

"""

import ika
import sprite
from direction import direction
from data import data
from PodSixNet.Connection import ConnectionListener, connection
from mapdata import mapData

class Entity(ConnectionListener):
	
	def __init__(self, id, name, x, y):
		
		self.name = name
		self.id = id
		self.sprite = sprite.Sprite("test")
		self.player = 0
		
		self.x = x
		self.y = y
		
		print x,y,self.x,self.y
		
		self.moveQueue = MoveQueue(self)

	def Draw(self):
		
		#print self.x, self.y
		
		data.fonts["system"].Print(self.x, self.y-10, self.name)
		self.sprite.Draw(self.x, self.y)
		
	def Update(self):
		
		if self.player:
			if self.moveQueue.IsNearEmpty():
				##add collision detection
				if ika.Input.keyboard["UP"].Position():
					connection.Send({'action':'Move', 'direction':direction["up"].number})
					self.moveQueue.Append(direction["up"])
					
				elif ika.Input.keyboard["DOWN"].Position():
					connection.Send({'action':'Move', 'direction':direction["down"].number})
					self.moveQueue.Append(direction["down"])
					
				elif ika.Input.keyboard["LEFT"].Position():
					connection.Send({'action':'Move', 'direction':direction["left"].number})
					self.moveQueue.Append(direction["left"])
					
				elif ika.Input.keyboard["RIGHT"].Position():
					connection.Send({'action':'Move', 'direction':direction["right"].number})
					self.moveQueue.Append(direction["right"])
					
		self.sprite.Update()
		self.moveQueue.ProcessQueue()
					
		self.Pump()
			
			
	def Network_Move(self, data):
		#id, direction
		#Direction is an integer mapping to the direction object's index.
		#Adds a direction to the move Queue.
		
		if data['id'] == self.id:
			self.moveQueue.Append(direction[data['direction']])
		
		
	def Network_SetPosition(self, data):
		#id,x,y,direction
		if data['id'] == self.id:
			self.x = data['x']
			self.y = data['y']
			self.direction = data['direction']
		
class MoveQueue:
	
	def __init__(self, entity):
		
		self.queue = [ ]
		self.entity = entity
		self.speed = 2
		self.progress = 0
		
	def IsNearEmpty(self):

		if len(self.queue) == 1 and self.progress+(self.speed*3) >= mapData.tileHeight:
			return 1
		elif len(self.queue) == 0:
			return 1
		else:
			return 0
		
	def IsEmpty(self):
		if len(self.queue) == 0:
			return 1
		return 0
		
	def Append(self, command):

		self.queue.append(command)
		
	def ProcessQueue(self):
		#Moves our entity as specified by the queue.	
		
		if len(self.queue) > 0:
			
			if self.queue[0] == direction["up"]:
				self.entity.y -= self.speed
				self.progress += self.speed
				
				if self.progress > mapData.tileHeight: #We're done moving
					#re-center on tile if the speed isn't evenly in the tile size.
					self.entity.y += self.progress - mapData.tileHeight 
					self.progress = 0
					self.queue.pop(0)
				
			elif self.queue[0] == direction["down"]:
				self.entity.y += self.speed
				self.progress += self.speed
				
				if self.progress > mapData.tileHeight: #We're done moving
					#re-center on tile if the speed isn't evenly in the tile size.
					self.entity.y -= self.progress - mapData.tileHeight 
					self.progress = 0
					self.queue.pop(0)
				
			elif self.queue[0] == direction["left"]:
				self.entity.x -= self.speed
				self.progress += self.speed
				
				if self.progress > mapData.tileHeight: #We're done moving
					#re-center on tile if the speed isn't evenly in the tile size.
					self.entity.x += self.progress - mapData.tileHeight 
					self.progress = 0
					self.queue.pop(0)
				
			elif self.queue[0] == direction["right"]:
				self.entity.x += self.speed
				self.progress += self.speed
				
				if self.progress > mapData.tileHeight: #We're done moving
					#re-center on tile if the speed isn't evenly in the tile size.
					self.entity.x -= self.progress - mapData.tileHeight 
					self.progress = 0
					self.queue.pop(0)
