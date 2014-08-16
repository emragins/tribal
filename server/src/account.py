import date

"""
TODO:
-Integrate with netcode (either directly or indirectly)
-stuff I haven't thought of
-finish 'lastSeen' workings -- really should be handled elsewhere
-finish warnReasons (need input box for gms and then some)

OTHER THOUGHTS:
-maybe should ask for info about real name? 
	don't think it matters unless we get big
-maybe should log IPs used?

-lastSeen to be used if player hasn't been around in, say, two weeks, 
	so that account can be set to inactive and character can be 
	removed/taken over (maybe taken over after far enough into game.  
	Needed for those who try game and hate it
-should add vacation mode (of, say, a month?) to keep this from happening to 
	serious players
-not sure exactly how 'inactive' will be used, but figure it'd be necessary in case
	somebody's stuff got deleted, they can still log in and see what happened
	
-deleting characters: I figure not allowed with the way the world is set up.
	We should probably make this very clear on character creation so that 
	people like X won't be all "whine whine whine" when they can't remake and
	change their looks. 
"""

class Account:
	def __init__(self, name, pass):
		self.name = name
		self.password = pass
		
		self.createdOn = date.today()	#untested but should work
		
		self.entity = None
		
		self.privalege = 'player'	#other options: 'gm', 'admin', ?
		self.active = True
		self.lastSeen = date.today()	
		
		self.warnings = 0
		self.warnReasons = []
		self.banned = False		
		self.bannedOn = []		#list of date strings of all bans
		
	#probably has to be handled elsewhere
	def Delete(self):
		self.active = False
		del self
		
	#possibly pointless depending how doing login.
	#at the moment I'm thinking list of accounts, then can check
	#password directly.  I think you have bigger plans.  
	#Might also be security issues doing it this way--I don't know.
	def CheckPassword(self, testWord):
		if testWord == self.password:
			return True
		return False
		
	def MakeNewCharacter(self):
		if self.entity == None:
			pass #let user make character
	
	def Warn(self):
		self.warnings += 1
		#self.warnReasons: get input and append to list
		if self.warnings == 3:
			self.Ban()
	def Unwarn(self):
		if self.warnings > 0:
			self.warnings -= 1
			self.warnReasons.pop()
			
	def Ban(self):
		self.banned = True
		self.bannedOn.append(str(date.today()))
	def Unban(self):
		self.warnings = 0
		self.warnReasons = []
		self.banned = False
	