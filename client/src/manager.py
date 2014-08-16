class Manager:
	"""
		Maintains a dictionary of objects to draw and update.
	"""
	
	"""
	'dictionary changed sizes during iteration'
	
	Unless you know a way around this, or maybe I'm just doing something wrong,
	we are going to have to change the manager's items to lists instead. 
	With the way things are set up, I don't think it would make a difference, anyway.
	"""
	
	def __init__(self):
		
		self.dict = {}
		
	def Get(self, key):
		return self.dict[key]
		
	def Add(self, key, value):

		self.dict[key] = value
		
	def Remove(self, key):
		
		del self.dict[key]
	
	def Update(self):

		for key, obj in self.dict.iteritems():
			
			obj.Update()
			
		for key, obj in self.dict.items():	
			if hasattr(obj, "dead") and obj.dead:
				del self.dict[key]		
		
	def Draw(self):
		
		for key, obj in self.dict.iteritems():
			
			obj.Draw()