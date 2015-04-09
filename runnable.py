class Runnable:
	"""
	The superclass for every class that wants to be added to the Application run loop
	"""
	def __init__(self):
		pass

	def tick(self, keypressEvent):
		"""
		Run the task that should be completed repeatedly

		Return False to remove self from the run loop
		"""
		return False

	def scroll(self, up):
		pass

	def click(self, x, y, button, press):
		pass

	def render(self, screen):
		pass

	def mouseMove(self, event):
		pass
	def click(self, x, y, button, press):
		pass
