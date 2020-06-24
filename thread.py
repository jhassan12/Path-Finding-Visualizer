class Thread:
	def __init__(self):
		self.is_threading = False
		self.is_finding_path = False
		self.finished_state = False
		self.path_exists = True

	def turn_on(self):
		self.is_threading = True
		self.is_finding_path = True

	def turn_off(self):
		self.is_threading = False
		self.is_finding_path = False
		self.finished_state = True

	def stop_search(self):
		self.is_finding_path = False

	def path_not_found(self):
		self.path_exists = False

	def reset_path_exists(self):
		self.path_exists = True

	def reset_finished_state(self):
		self.finished_state = False




