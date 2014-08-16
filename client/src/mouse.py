import ika
import timer

"""
Other programs may see mouse function by calling ___clicked, ___held, ___released
For Clicked and Released, the using program must send a message back to the mouse that 
the click/release was used via the ________Used functions.  (Maybe this should change)

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
		
		#will be used (indirectly) by others to determine state of mouse
		self.leftClicked = False
		self.leftHeld = False
		self.leftReleased = False
		
		self.rightClicked = False
		self.rightHeld = False
		self.rightReleased = False
		
		self.middleClicked = False
		self.middleHeld = False
		self.middleReleased = False
		
	def LeftClick(self):
		return self.leftClicked
	def LeftHeld(self):
		return self.leftHeld
	def LeftReleased(self):
		return self.leftReleased
	def LeftClickUsed(self):
		self.leftClicked = False
	def LeftReleaseUsed(self):
		self.leftReleased = False
	
	def RightClick(self):
		return self.rightClicked
	def RightHeld(self):
		return self.rightHeld
	def RightReleased(self):
		return self.rightReleased
	def RightClickUsed(self):
		self.rightClicked = False
	def RightReleaseUsed(self):
		self.rightReleased = False
	
	def MiddleClick(self):
		return self.middleClicked
	def MiddleHeld(self):
		return self.middleHeld
	def MiddleReleased(self):
		return self.middleReleased	
	def MiddleClickUsed(self):
		self.middleClicked = False
	def MiddleReleaseUsed(self):
		self.middleReleased = False
	
	
	def Draw(self):
		self.pointer.Blit(int(self.mouse.x.Position()), int(self.mouse.y.Position()))
		
	def Update(self):
		self.x = int(self.mouse.x.Position())
		self.y = int(self.mouse.y.Position())
		
				
		if self.mouse.left.Position():
			if self.leftPressed is False:
				self.leftClicked = True
				#print 'A clicked left button at', self.x, self.y	###
				
				self.timer.Reset()
				self.leftPressed = True
			elif self.leftPressed and self.timer.IsDone():
				self.leftHeld = True
				#print 'held left button at', self.x, self.y	###
		
		if self.mouse.right.Position():
			if self.rightPressed is False:
				self.rightClicked = True
				self.timer.Reset()
				self.rightPressed = True
			elif self.rightPressed and self.timer.IsDone():
				self.rightHeld = True
				print 'held right button at', self.x, self.y	###
		
		if self.mouse.middle.Position():
			if self.middlePressed is False:
				self.middleClicked = True
				self.timer.Reset()
				self.middlePressed = True
			elif self.middlePressed and self.timer.IsDone():
				self.middleHeld = True
				print 'held middle button at', self.x, self.y	###
		
		
		if self.mouse.left.Position() == 0 and self.leftPressed:
			self.leftPressed = False
			self.leftReleased = True
		if self.mouse.right.Position() == 0 and self.rightPressed:
			self.rightPressed = False
			self.rightReleased = True
		if self.mouse.middle.Position() == 0 and self.middlePressed:
			self.middlePressed = False
			self.middleReleased = True
			
mouse = Mouse()