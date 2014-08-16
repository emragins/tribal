import shelve

'''
NOTE: Hard-coded key is the filename
Option now exists to use hard-coded keys in rest of program
-must use save/loadKey instead of read/write
'''

class Shelf:
	def __init__(self, filename = None):
		self.filename = filename
		self.isOpen = 0
		self.operator = None
		self.key = str(self.filename)
		
	def Open(self, filename = None):
		if filename is None:	
			filename = self.filename
		self.ChangeFiles(filename)
		self.operator = shelve.open(self.filename)
		self.isOpen = 1
		
	def Close(self):
		self.operator.close()
		self.isOpen = 0
		
	def IsOpen(self):
		return self.isOpen
		#poor work-around... may not work if closes unexpectedly in app.
	
	def Read(self, filename = None):
		if filename is None:	
			filename = self.filename
		if self.isOpen == False:
			print 'file not open. opening then reading...'
			self.open(filename)
		value = self.loadKey()
		return value
		
	def Write(self, value):
		self.saveKey(self.key, value)
		
	def SaveKey(self, key = None, value = None):
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
			
	def LoadKey(self, key = None):
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
			
	def ChangeFiles(self, newFilename):
		self.filename = newFilename
		self.key = str(self.filename)