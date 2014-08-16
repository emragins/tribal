import sys
sys.path = ['','src','images','sound','music','python','python\win32','python\\pywin32_system32']

import engine
import ika

from PodSixNet.Connection import ConnectionListener, connection
from engine import engine
from data import data
from mapengine import mapEngine
from window import windowManager
import chat


class ConnectionWrapper:
	
	def Update(self):
		connection.Pump()
	def Draw(self):
		pass

def main():

	connection.DoConnect(('localhost', 9126))

	eng = engine
	chatbox = chat.ChatBox()
	eng.AddObject('con. wrapper', ConnectionWrapper())
	#eng.AddObject('chatbox', chatbox)
	#eng.AddObject('map engine', mapEngine)
	eng.AddObject('window manager', windowManager)
	
	
	##testing stuff
	import menu
	win = menu.Menu(50,50)
		
	eng.mainLoop()

main()