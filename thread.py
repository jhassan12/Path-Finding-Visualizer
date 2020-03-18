class Thread:
	def __init__(self):
		self.is_threading = False

	def turn_on(self):
		self.is_threading = True

	def turn_off(self):
		self.is_threading = False