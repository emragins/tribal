from PodSixNet.Channel import Channel
import message

#network channel of a single client
#refers to server when needing to communciate with other clients
#can directly communicate with its own client using Send()
#receivess messages from its particular client with Network_ functions

class ClientChannel(Channel):

	def __init__(self, *args, **kwargs):
		self.player = None
		Channel.__init__(self, *args, **kwargs)
	
	#called when client does connection.Send(data)
	def Network(self, data):
		print data	#prints in server window (despite being in client thing)
		
	#called when client closes (or rather, disconnects)
	def Close(self):
		print self.name, 'connection left'
		self._server.removePlayer(self)
		self._server.messageToAll("%s has left!" % self.name)

	def Network_AllChat(self, message):
		
		msg = message.Chat("<%s> %s" % (self.name,message['text']))
		
		self._server.SendToAllExcept(self.name, msg)
		
	def Network_Login(self, message):
		print 'calling network_login in channel'	##doesn't exist (yet) in chat client
		if not self._server.playerExists(data['name']):	#if player name doesn't exist already
			self.name = data['name']
			self._server.messageToAll("%s has joined!" % self.name)
			
	@property
	def name(self):
		return self.Player.name
			
	