from PodSixNet.Channel import Channel
import messages
import entity
from mapmanager import mapManager

from rencode import loads, dumps

#network channel of a single client
#refers to server when needing to communciate with other clients
#can directly communicate with its own client using Send()
#receivess messages from its particular client with Network_ functions

class AuthenticationChannel(Channel):
	"""
		Adds logged in / not logged in states to a channel to determine what 
		Network_<x> functions it can access.
		
		Expects a loggedIn boolean attribute.
	"""
	
	guestFunctions = []
	
	def found_terminator(self):
		#This is very tied-down to podsix's implementation so we'll need to keep it consistent as podsix updates.
		
		data = loads(self._ibuffer)
		self._ibuffer = ""
		
		if type(dict()) == type(data) and data.has_key('action'):
			self.NetworkAuth(data)
		else:
			print "OOB data:", data	
			
	def NetworkAuth(self,message):

		if self.loggedIn:
			[getattr(self, n)(message) for n in ('Network_' + message['action'], 'Network') if hasattr(self, n)]
		else:
			if message['action'] in self.guestFunctions:
				[getattr(self, n)(message) for n in ('Network_' + message['action'], 'Network') if hasattr(self, n)]
			else:
				print "Unauthorized function attempt by %s: %s"  % (str(self.addr), str(message))

class ClientChannel(AuthenticationChannel):
	
	guestFunctions = ['Login', 'Chat'] #functions that not logged in users can access.

	def __init__(self, *args, **kwargs):
		self.entity = None
		self.loggedIn = False
		
		Channel.__init__(self, *args, **kwargs)
		
		self.Send(messages.Chat("You are connected. Use /login <name> <pass> to login."))
	
	#called when client does connection.Send(data)
	def Network(self, message):
		pass
		#print "Unhandled message from %s: %s" % (str(self.addr), message)
		
	#called when client closes the connection
	def Close(self):
		if self.loggedIn:
			print "%s logged off." % self.name
			self._server.LogOut(self.name)
			self.entity.channel = None ##need to make this an entity function
		else:
			print "%s disconnected prior to login." % str(self.addr)
			self._server.LogInCancelled(self)

	def Network_Chat(self, message):
		#message: text
		
		if message['text'] == "":
			return 1
		
		if message['text'][0] == "/": #Command processing if it starts with a backslash.
			command = message['text'].split()
			try:
				if command[0] == "/login":
					##temporary fix until we have a real client login.
					if self.loggedIn == False:
						self.Network_Login({"name": command[1], "password": command[2]})
			except IndexError:
				self.Send(messages.Chat("Invalid command format."))
			
		elif self.loggedIn:
			print "(All) (%s) %s" % (self.name, message['text'])
			
			msg = messages.Chat("<%s> %s" % (self.name,message['text']))
		
			##Temporarily disabled until the client echoes text
			#self._server.SendToAllExcept(self.name, msg)
			self._server.SendToAll(msg)
		
	def Network_Login(self, message):
		#message: name, password
		
		##Add network authentication
		
		name = message['name']
		
		if not self._server.ChannelActive(name): #Make sure that player isn't already logged in.
			##I hate everything about this
			if self._server.playerEntities.has_key(name):
				self.entity = self._server.playerEntities[name]
				self.entity.channel = self ##need to make this an entity func
				
			else:
				ent = entity.Entity(name, "e"+name, 0,0)
				ent.channel = self
				self._server.playerEntities[name] = ent
				self.entity = ent
			
			self.entity.SetMap(mapManager.maps[0][0])
			
			self._server.LogIn(name, self)
			self.loggedIn = True
		else:
			self.Send(messages.Chat("You're already logged on"))
			#self.close()
			#self._server.LogInCancelled(self)
			
	def Network_Move(self, message):
		#direction
		##I'm not sure I like that the channel translates messages to
		##the entities. Passing relevant messages may be a better approach.
		
		print 'move received'
		
		if not self.entity.Move(message['direction']): #if moving failed...
			##should move this back into the entity.
			self.Send(messages.SetPosition(self.entity.id, self.entity.x, self.entity.y, 0))
			
			
	@property
	def name(self):
		#return "anonymous" ##temporary fix until we have actual entities to use.
		return self.entity.name
			
	