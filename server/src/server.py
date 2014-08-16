from PodSixNet.Server import Server

import time
import channel
import sys
import messages
from mapmanager import mapManager


'''
Need to figure out what should be handled by the server and what by the clientchannel.
It seems like you're trying to do a lot via the client channel--stuff that maybe would
be better left to the server.  For instance, in Close(), I agree that the client has to tell the server
that it's leaving (how else would it know?,) but shouldn't the server know, "hey, this guy left, I 
better tell everybody else"?  Same with login.
'''


"""
TODO:
	Each player has name... name should be chosen/assigned/whatever when player opens client.
	Maybe would have to have preliminary connection to server to achieve the whole login effect.
	
	Need to make effective input-type box since useful python functions like "raw_input()" are shot dead 
		thanks to ika.
	
Other:
	I don't see where client knows to connect to local host.
	Otherwise I *think* I have at least a working understanding of how this goes... please correct if my
		surmised comments are off.
"""

class GameServer(Server):
	
	channelClass = channel.ClientChannel

	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		
		self.gameChannels ={} #Dictionary mapping channels to their account name.
		#It's named gameChannels because PodSix uses channels.
		self.loginChannels = [] #List of channels that haven't logged in yet.
		
		self.playerEntities = {} ##Temporary list of player entities.
		
		print 'Server launched'

	#------------------------------------------------------------------------------
	#Channel management
	#------------------------------------------------------------------------------

	def Connected(self, channel, addr):
		print "Connection from %s" % (str(addr))
		
		self.loginChannels.append(channel)

	def LogIn(self, name, channel):
		
		print "%s logged in" % (name)
		
		self.loginChannels.remove(channel)
		
		self.gameChannels[name] = channel
		
		self.SendToAll(messages.Chat("%s has joined!" % name))
		
	def LogOut(self, name):
		
		if self.gameChannels.has_key(name):
		
			del self.gameChannels[name]
			
	def LogInCancelled(self, channel):
		
		self.loginChannels.remove(channel)
			
	def ChannelActive(self, name):
		
		return self.gameChannels.has_key(name)
		
	#------------------------------------------------------------------------------
	#Communcation functions.
	#------------------------------------------------------------------------------
		
	def SendToList(self, names, message):

		for name in names:
			
			if self.gameChannels.has_name(name):
				self.gameChannels[name].Send(message)
				
		
	def SendToAllExcept(self, name, message):
		
		for cname, c in self.gameChannels.iteritems():
			
			if cname != name:
				
				c.Send(message)
		
	def SendToAll(self, message):
		
		for c in self.gameChannels.itervalues():
			
			c.Send(message)

	#------------------------------------------------------------------------------
	#Main Loop
	#------------------------------------------------------------------------------

	def Launch(self):
		while True:
			self.Pump()
			time.sleep(0.0001)

			
server = GameServer(localaddr=("", 9126))
