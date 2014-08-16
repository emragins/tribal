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
	
	def __init__(self, id, x, y):
		
		self.id = id
		self.sprite = sprite.Sprite("test")
		self.player = 0
		
		self.x = x
		self.y = y
		
		self.moveQueue = MoveQueue(self)

	def draw(self):
		
		data.fonts["system"].Print(self.sprite.x, self.sprite.y-10, self.id)
		self.sprite.Draw(self.x, self.y)
		
	def update(self):
	
		self.sprite.update()
		self.moveQueue.processQueue()
		
		if self.player:
			if self.moveQueue.isEmpty():
				
				#if up and no collision up
					connection.Send({'action':'move', 'direction':direction["up"].number})
					self.moveQueue.append(direction["up"])
				#elif down and no collision down
					connection.Send({'action':'move', 'direction':direction["down"].number})
					self.moveQueue.append(direction["down"])
				#elif left and no collision left
					connection.Send({'action':'move', 'direction':direction["left"].number})
					self.moveQueue.append(direction["left"])
				#elif right and no collision right
					connection.Send({'action':'move', 'direction':direction["right"].number})
					self.moveQueue.append(direction["right"])
			
			
	def Network_move(self, data):
		#id, direction
		#Direction is an integer mapping to the direction object's index.
		#Adds a direction to the move Queue.
		
		if data['id'] == self.id:
			self.moveQueue.append(direction[data['direction']])
		
		
	def Network_setPosition(self, data):
		#id,x,y,direction
		if data['id'] == self.id:
			self.x = data['x']
			self.y = data['y']
			self.direction = data['direction']
		
class MoveQueue:
	
	def __init__(self, entity):
		
		self.queue = [ ]
		self.entity = entity
		self.speed = 5
		self.progress = 0
		
	def isEmpty(self):
		if len(self.queue) == 0:
			return 1
		return 0
		
	def append(self, command):

		self.queue.append(command)
		
	def processQueue():
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
				
			if self.queue[0] == direction["down"]:
				self.entity.y += self.speed
				self.progress += self.speed
				
				if self.progress > mapData.tileHeight: #We're done moving
					#re-center on tile if the speed isn't evenly in the tile size.
					self.entity.y -= self.progress - mapData.tileHeight 
					self.progress = 0
					self.queue.pop(0)
				
			if self.queue[0] == direction["left"]:
				self.entity.x -= self.speed
				self.progress += self.speed
				
				if self.progress > mapData.tileHeight: #We're done moving
					#re-center on tile if the speed isn't evenly in the tile size.
					self.entity.x += self.progress - mapData.tileHeight 
					self.progress = 0
					self.queue.pop(0)
				
			if self.queue[0] == direction["right"]:
				self.entity.x += self.speed
				self.progress += self.speed
				
				if self.progress > mapData.tileHeight: #We're done moving
					#re-center on tile if the speed isn't evenly in the tile size.
					self.entity.x -= self.progress - mapData.tileHeight 
					self.progress = 0
					self.queue.pop(0)
