import time

class Timer:
	"""
		Sets a current time and duration to be used 
		to tell whether that time has passed yet. 
		
		Mostly for timing stuff that takes time on the client end
		but doesn't really exist for the server.
	"""
	
	def __init__(self, duration):
		"""
			Starts the timer. Duration is the length it lasts.
		"""
		
		
		self.startTime = time.time()
		self.duration = duration
		self.endTime = self.startTime+duration
		
		self.Reset()
		
	def Reset(self):
		"""
			Resets the start and end times based on
			the original duration of the timer.
		"""
		
		
		self.startTime = time.time()
		self.endTime = self.startTime+self.duration
		
	def IsDone(self):
		"""
			Returns true or false depending on whether the 
			timer's designated end time has passed.
		"""
		
		if self.endTime < time.time():
			return True
		else:
			return False