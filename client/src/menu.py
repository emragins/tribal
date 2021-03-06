import ika
import window
from data import data
import box

"""
Part of me has the sinking feeling that I'm reinventing the wheel yet again.

TODO:
-(X) - switch x/y coords to offsets of initial x/y
-(X) - UNTESTED - center cursor in middle (vertically) of slot 
-add option for menu to have a header 
	-if list['header']....
		-put in first slot... then would have to always check if new selected
		slot was actually a header, and that sounds stupid, so...
	-just add a 'header' class attribute and have it diplay fontHeight
	above given x,y (or something)
-( ) - add option to display tooltips (value in dict.. will have to distinguish somehow
	between tooltip value and 'make new submenu' value)
-(X) - UNTESTED - change position of menu to set x/y coords instead of
	trying to center on screen. That entire FigureAndSetXY() should probably
	be revamped.
	(user movable? ...no. that would be controlled by another class if/when implemented) 
-( ) - tweak borders so a) not off center b) can be pretty (don't know how)
-( ) - add mouse functionality
-( ) - possibly compact SelectionMade() into Menu() as indicated in note (near bottom)
-( ) - alter cursor image handling so that inventory lists could have unique graphics 
	for each type of item. (Have all types of cursors listed initialized in (specific) menu class,
	then have it pass argument to Slot as to which type of cursor to use, where it would be initialized.)
-( ) - add functionality for 'right' and 'left' options in menus (submenus)
-( ) - add horizontal display option with pictures


If needed:
-( ) - add functionality (possibly) such that a list (not dict) could be 
	used instead with blank tooltips (ie. probably just turn list into dict
	then procede as usual)
-( ) - add functionality for multiple selections (probably define is specific class, or have new MenuMulti option)
"""


"""
Menu
-----------------------------
| -C1- 	| Slot1 key 		|
-----------------------------
|**C2**	| Slot2 key 		|
-----------------------------

Message Box (class elsewhere)
-----------------------------
| Slot2 value (tooltip)shows|
-----------------------------


What a menu needs:
- boxes for text and/or pictures
- an action to take when a box is selected
	-choosing an option
	-opening new menu
	-something completely different
- a way for boxes to be selected (keyboard/mouse)
	-keyboard	
		-basic navigation
		-'enter' function
	-mouse
		-'click in box' detection
- tooltips
	-mouse-over (for pictures only?  good for UI)
	-seperate tooltip box (better for inventory)
- layout
	-vertical
	-horizontal
	-???
- a way to grow/shrink/have multiple pages/??? for various list sizes
- have x/y coords defined solely by offsets


Kind of 'menus' that will be seen:
	-game menu
	-inventory
	-dialogue type stuff
	-store-type-things
	-specialty building options
	-crafting stuff
"""

cursors = {'default': ika.Image('images\\default cursor.png')
			}
class TooltipBox:
	def __init__(self, x, y):
		pass
			
class Slot(box.Box):
	def __init__(self, xOffset, yOffset, text, parent, type = 'default'):
		self.xOffset = xOffset
		self.yOffset = yOffset
		self.width = parent.width
		self.height = parent.slotHeight
		
		box.Box.__init__(self, self.xOffset, self.yOffset, self.width, self.height)
		
		self.margin = parent.margin
		self.font = parent.font
		
		global cursors
		self.cursor = cursors[type]
		self.cursorOffset = parent.cursorOffset #used in the event text is bigger than cursor
		
		self.textXOffset = self.xOffset + self.cursor.width + self.margin
		self.textYOffset = self.yOffset
		
		self.text = text
		self.tooltip = parent.list[text]
		self.selected = False
		
	def Draw(self, givenX, givenY):	#these are coords of parent's x, y
		if self.selected:
			self.cursor.Blit(givenX + self.xOffset, givenY + self.yOffset + self.cursorOffset)
		self.font.Print(givenX + self.textXOffset, givenY + self.textYOffset, self.text)
	

"""
base Menu class does not initiate inheritance to a subwindow.  It could, but then it would have to take
'id' as an arguement--easily changed if that is desired.
"""
	
class Menu(window.Subwindow):
	def __init__(self, x, y, list = {'this': 'this tip', 'a': 'a tip', 'menu': 'menu tip'}):
		self.font = data.fonts["system"]
		self.id = 'default menu'
		
		#Note:
		#The keys are what is displayed
		#the program operates with the keys
		#values are used for possible tooltips and/or submenus
		self.list = list
		
		self.menuOptions = self.list.keys()
		
		
		
		#--Establish boundaries of menu and slots-------------
		global cursors
		self.cursor = cursors['default']
		self.cursorOffset = 0
		
		self.margin = 5 ##
		#these values are set in stone.. they are simply there to be initialized
		self.width = 0
		self.height = 0
		
		##cursor size will probably have to be set in stone for specific menus (nullifying this?)
		##ideally the cursor shouldn't be taller than the text anyway
		self.slotHeight = max(self.font.height, self.cursor.height)	
		if self.slotHeight > self.cursor.height:
			dif = self.slotHeight - self.cursor.height
			self.cursorOffset = int(dif/2)
		
		self.FigureWidthAndHeight()
		#-----------------------------------------------------
		
		
		self.slots = []	
		self.MakeSlots()
		
		self.currentSelection = 0
		self.InitializeSelectedSlot()
		
		
	def Update(self):
		kb = ika.Input.keyboard
		
		if kb["UP"].Pressed():
			self.CursorUp()
		if kb["DOWN"].Pressed():
			self.CursorDown()
		if kb["RETURN"].Pressed():
			self.SelectionMade()
			
	def Draw(self, givenX, givenY):
		#border
		ika.Video.DrawRect(givenX-1, givenY-1, givenX + self.width + 1, givenY + self.height + 1, data.colors['white'], 0)
		#internal box
		ika.Video.DrawRect(givenX, givenY, givenX + self.width, givenY + self.height, data.colors['dark blue'], 1)
		
		for slot in self.slots:
			slot.Draw(givenX, givenY)
		
	#coords received are given as if window is at (0,0)
	def ReceivedLeftClick(self, x, y):
		#establish which slot corrosponds
		slot_match = 0
		for i, slot in enumerate(self.slots):
			if slot.HasPoint(x, y):
				slot_match = i
				break
		self.currentSelection = slot_match
		self.SelectionMade()
		
		
	def FigureWidthAndHeight(self):
		#figure width
		max_string_width = 0
		for option in self.menuOptions:
			w = self.font.StringWidth(option)
			if w > max_string_width:
				max_string_width = w
		#set width
		self.width = max_string_width + 3*self.margin + self.cursor.width
		
		#figure height
		needed_text_y = len(self.menuOptions)*(self.slotHeight)
		#set height
		self.height = needed_text_y + 2*self.margin
	
	def MakeSlots(self):
		x_offset = self.margin
		y_offset = self.margin
		
		for i, option in enumerate(self.menuOptions):
			new_slot = Slot(x_offset, y_offset, option, self)
			self.slots.append(new_slot)
			y_offset += self.slotHeight
	
	def InitializeSelectedSlot(self):
		self.slots[self.currentSelection].selected = True
		
	def CursorUp(self):
		#note: does not act on a cursor, but rather tells selected slot to display cursor
		print 'cursor up' ##
		print self.currentSelection ##
		
		self.currentSelection -= 1
		try:
			self.slots[self.currentSelection].selected = True
			self.slots[self.currentSelection+1].selected = False
		except:
			self.currentSelection += 1
		print self.currentSelection ##
		
	def CursorDown(self):
		#note: does not act on a cursor, but rather tells selected slot to display cursor
		print 'cursor down' ##
		print self.currentSelection##
		self.currentSelection += 1
		try:
			self.slots[self.currentSelection].selected = True
			self.slots[self.currentSelection-1].selected = False
		except:
			self.currentSelection -= 1
		print self.currentSelection	##
		
		
	#note: could not override SelectionMade and instead use: self.calls = CallThisFunction
	def SelectionMade(self):
		slot = self.slots[self.currentSelection]
		key = slot.text
		program_code = self.list[key]
		print 'selected default menu item', program_code
		self.Die()


		
class Menu1(Menu):
	def __init__(self, x, y):
		Menu.__init__(self,x, y)
		self.id = 'menu1'
		window.Subwindow.__init__(self, x, y, self.width, self.height, self.id)

class Menu2(Menu):
	def __init__(self, x, y):
		Menu.__init__(self,x, y)
		self.id = 'menu2'
		window.Subwindow.__init__(self, x, y, self.width, self.height, self.id)

class Menu3(Menu):
	def __init__(self, x, y):
		Menu.__init__(self,x, y)
		self.id = 'menu3'
		window.Subwindow.__init__(self, x, y, self.width, self.height, self.id)
		
""" 
Sample	 (Unfinished)
	
class EquipmentMenu(Menu):
	def __init__(self):
		#could also have it pop up new box just saying current equipment
		list = {'Head': Menu(ListOfPlayersHeadShit),	 # would initialize with current equipment as selected value
				'Body': Menu(ListOfPlayersBodyShit),	
				'R. Hand': Menu(ListOfPlayersHandShit),
				'Strip': 'Instantly remove all clothing'
				}
		Menu.__init__(self, list)
	
	def SelectionMade(self):
		slot = self.slots[self.currentSelection]
		key = slot.text
		program_code = self.list[key]
		from game import SetSpeed
		SetSpeed(program_code)
		data.gains_control.remove(self)
"""