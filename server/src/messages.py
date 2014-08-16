
##Considering moving any of these that only occur in a single class to that class's module.

def Chat(text):
	
	return {"action": "Chat", "text": text}
		
def Move(id, direction):
	
	return {"action": "Move", "id": id, "direction": direction}
		
def AddEntity(id,name,x,y):
	
	return {"action": "AddEntity", "id": id, "name": name, "x": x, "y": y}
		
def SetPlayer(id):
	
	return {"action":"SetPlayer", "id": id} 
		
def SetPosition(id,x,y,dir):
	
	return {"action":"SetPosition", "id": id, "x": x, "y": y, "direction": dir} 