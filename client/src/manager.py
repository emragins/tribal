class Manager:
	"""
		Maintains a dictionary of objects to draw and update.
	"""
		
	def __init__(self):
		
		self.dict = {}
		
	def Has(self, key):

		return self.dict.has_key(key)
		
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