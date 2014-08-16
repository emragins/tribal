"""#SDHawk
class dir: #Simple struct-like class for storing constants of the directions. Also contains lists for other purposes
	
	Up = 0
	Down = 1
	Left = 2
	Right = 3
	
"""

class Direction:
	def __init__ (self, movescript, animation,number):
		self.movescript = movescript
		self.animation = animation
		self.number = number

direction =	{
			"up": Direction("u", "up",0),
			"down": Direction("d", "down",1),
			"left": Direction("l", "left",2),
			"right": Direction("r", "right",3),
		}
		
direction["up"].opposite = direction["down"]
direction["down"].opposite = direction["up"]
direction["left"].opposite = direction["right"]
direction["right"].opposite = direction["left"]

direction[0] = direction["up"]
direction[1] = direction["down"]
direction[2] =direction["left"]
direction[3] = direction["right"]