import sys
sys.path = ['','src', 'src\\ui', 'images','sound','music','python','python\win32','python\\pywin32_system32']

import engine
import ika

from PodSixNet.Connection import ConnectionListener, connection
from data import data
from engine import engine
from mapengine import mapEngine
from mouse import mouse
from windowmanager import windowManager
import chat


##take me out later
def AddTestWindows():
	import menu
	import loginmenu
	menu.Menu1(200,200)
	loginmenu.LoginMenu(300,300)
	menu.Menu3(400,400)


class ConnectionWrapper:
	
	def Update(self):
		connection.Pump()
	def Draw(self):
		pass

def main():

	connection.DoConnect(('localhost', 9126))
	#connection.Send({"action": "Login", "name": "anonymous", "password":""})

	eng = engine
	chatbox = chat.ChatBox()
	
	"""
	numbers on end for priority  where '0' is highest (namely of drawing)
	presently only have 3 layers. Easy to add more, you'll see how if you want.
	"""
	
	eng.AddObject('mouse', mouse, 0) #mouse needs to be first or things look funny..
	
	eng.AddObject('con. wrapper', ConnectionWrapper(), 1)
	
	eng.AddObject('map engine', mapEngine, 2)
	eng.AddObject('window manager', windowManager, 1)
	
	AddTestWindows()##take me out later
	
	eng.MainLoop()
	
main()

