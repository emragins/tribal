import ika
import timer

"""
Other programs may see mouse function by calling ___clicked, ___held, ___released

At present the using program accesses x and y directly... maybe this, too, should change.

Alternative pointers should be as simple as changing the type of the pointer.. functionality for
practical use would need to be added.
"""

pointers = {
			"default": ika.Image("images\\default cursor.png")
			}
			
class Mouse:
	def __init__(self, type = 'default'):
		self.mouse = ika.Input.mouse
		
		self.x = int(self.mouse.x.Position())
		self.y = int(self.mouse.y.Position())
		self.type = type
		
		global pointers
		self.pointer = pointers[self.type]

		#used internally only
		self.leftPressed = False
		self.rightPressed = False
		self.middlePressed = False
		self.timer = timer.Timer(10)
		self.doubleTimer = timer.Timer(40)
		
		#will be used (indirectly) by others to determine state of mouse
		self.leftClicked = False
		self.leftDoubleClicked = False
		self.leftHeld = False
		self.leftReleased = False
		
		self.rightClicked = False
		self.rightDoubleClicked = False
		self.rightHeld = False
		self.rightReleased = False
		
		self.middleClicked = False
		self.middleDoubleClicked = False
		self.middleHeld = False
		self.middleReleased = False
		
	def LeftClick(self):
		return self.leftClicked
	def LeftDoubleClick(self):
		return self.leftDoubleClicked
	def LeftHeld(self):
		return self.leftHeld
	def LeftReleased(self):
		return self.leftReleased
	
	def RightClick(self):
		return self.rightClicked
	def RightDoubleClick(self):
		return self.rightDoubleClicked
	def RightHeld(self):
		return self.rightHeld
	def RightReleased(self):
		return self.rightReleased
	
	def MiddleClick(self):
		return self.middleClicked
	def MiddleDoubleClick(self):
		return middleDoubleClicked
	def MiddleHeld(self):
		return self.middleHeld
	def MiddleReleased(self):
		return self.middleReleased	
	
	
	def Draw(self):
		self.pointer.Blit(int(self.mouse.x.Position()), int(self.mouse.y.Position()))
		
	def Update(self):
		self.x = int(self.mouse.x.Position())
		self.y = int(self.mouse.y.Position())
		
		self.ResetState()
			
		if self.mouse.left.Position():
			if self.leftPressed is False and self.doubleTimer.IsDone() is False:
				self.leftDoubleClicked = True
				self.leftPressed = True
			elif self.leftPressed is False:
				self.leftClicked = True
				self.timer.Reset()
				self.doubleTimer.Reset()
				self.leftPressed = True
			elif self.leftPressed and self.timer.IsDone():
				self.leftHeld = True
		
		if self.mouse.right.Position():
			if self.rightPressed is False:
				self.rightClicked = True
				self.timer.Reset()
				self.rightPressed = True
			elif self.rightPressed and self.timer.IsDone():
				self.rightHeld = True
		
		if self.mouse.middle.Position():
			if self.middlePressed is False:
				self.middleClicked = True
				self.timer.Reset()
				self.middlePressed = True
			elif self.middlePressed and self.timer.IsDone():
				self.middleHeld = True
		
		
		if self.mouse.left.Position() == 0 and self.leftPressed:
			self.leftPressed = False
			self.leftReleased = True
		if self.mouse.right.Position() == 0 and self.rightPressed:
			self.rightPressed = False
			self.rightReleased = True
		if self.mouse.middle.Position() == 0 and self.middlePressed:
			self.middlePressed = False
			self.middleReleased = True
	
	def GetXY(self):
		return self.x, self.y
	
	def ResetState(self):
		#ideally in most common order
		#assumes only one action can be taken per update
		if self.leftClicked:
			self.leftClicked = False
		elif self.leftReleased:
			self.leftReleased = False
		elif self.leftDoubleClicked:
			self.leftDoubleClicked = False
		elif self.rightClicked:
			self.rightClicked = False
		elif self.middleClicked:
			self.middleClicked = False
		elif self.rightReleased:
			self.rightReleased = False
		elif self.rightDoubleClicked:
			self.rightDoubleClicked = False
		elif self.middleReleased:
			self.middleReleased = False
		elif self.middleDoubleClicked:
			self.middleDoubleClicked = False
		
mouse = Mouse()

##adding this to commit again