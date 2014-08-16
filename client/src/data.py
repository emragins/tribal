import ika

#from map import map
'''
this can't be here.  What are you trying to do with it?
Or rather.. whole circular thing with data -> map -> entity -> data needs to change
Chances are something's trying to use something it doesn't need--say, could they both use data
and not each other?  ( I don't know, haven't really looked.)
'''

class GameData:
	
	def __init__(self):
		
		self.fonts = {
					"system": ika.Font("system.fnt")
				}
				
		self.colors = {
					"white": ika.RGB(255,255,255),
					"black": ika.RGB(0,0,0),
					"dark blue": ika.RGB(0,0, 100),
					"light grey": ika.RGB(100, 100, 100),
					"red": ika.RGB(255, 0, 0)
				}
		
	
data = GameData()