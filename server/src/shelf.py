import shelve

'''
NOTE: Hard-coded key is the filename
Option now exists to use hard-coded keys in rest of program
-must use save/loadKey instead of read/write
'''

class Shelf:
	def __init__(self, filename = None):
		self.filename = filename
		self.is_open = 0
		self.operator = None
		self.key = str(self.filename)
		
	def open(self, filename = None):
		if filename is None:	
			filename = self.filename
		self.ChangeFiles(filename)
		self.operator = shelve.open(self.filename)
		self.is_open = 1
		
	def close(self):
		self.operator.close()
		self.is_open = 0
		
	def isOpen(self):
		return self.is_open
		#poor work-around... may not work if closes unexpectedly in app.
	
	def read(self, filename = None):
		if filename is None:	
			filename = self.filename
		if self.is_open == False:
			print 'file not open. opening then reading...'
			self.open(filename)
		value = self.loadKey()
		return value
		
	def write(self, value):
		self.saveKey(self.key, value)
		
	def saveKey(self, key = None, value = None):
		if key == None:
			key = self.key
		if self.isOpen() == False:
			self.open()
		
		try:
			self.operator[key] = value
			print 'in saveKey:', value, 'saved in', key ##----------
		except:
			print 'WARNING: in savekey; shelf writing exception'
			self.operator[key] = 'I AM HERE THANKS TO SAVE PROBLEM'
			
	def loadKey(self, key = None):
		if key == None:
			key = self.key
		if self.isOpen() == False:
			print 'in loadKey, opening file'
			self.open()
		
		value = None #init for use
		try:
			value = self.operator[key]
			print 'in loadKey:', value, 'loaded from', key ##----------
		except:
			print 'WARNING: in loadkey; shelf reading exception'
			value = 'I AM HERE BECAUSE KEY DOES NOT EXIST'
		return value
			
	def ChangeFiles(self, new_filename):
		self.filename = new_filename
		self.key = str(self.filename)